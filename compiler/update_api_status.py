"""OpenAPI 定義から MiPAC の対応状況・変更点・生成物を更新する

使い方:
    uv run python compiler/update_api_status.py [NEW_API_JSON]

NEW_API_JSON を渡すと datas/v13_api.json(現行)と比較して差分を表示し、
処理後に datas/v13_api.json を新しい定義で置き換える。
省略時は現行の定義から生成物だけを作り直す。

対応状況は mipac/ 内の Route("POST", "/api/...") を走査して自動判定する。

生成物:
    mipac/types/endpoints.py      ENDPOINTS の Literal 型
    mipac/errors/errors.py        エラークラス
    compiler/datas/errors.csv     エラー一覧
    compiler/datas/support_status.md
    compiler/datas/api_changes_report.html
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import pathlib
import re
import shutil
import sys
from typing import Any, Literal, TypedDict

COMPILER_PATH = pathlib.Path(__file__).resolve().parent
ROOT_PATH = COMPILER_PATH.parent
DATAS_PATH = COMPILER_PATH / "datas"
API_PATH = DATAS_PATH / "v13_api.json"

sys.path.insert(0, str(COMPILER_PATH))
from type import OpenAPI  # noqa: E402

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError:
    raise ImportError("Jinja2 が必要です。`uv sync` を実行してください") from None

STATUS = Literal["supported", "needToWork", "notSupported"]
STATUS_LABELS: dict[str, str] = {
    "supported": "完全対応",
    "needToWork": "要作業",
    "notSupported": "未対応",
    "RemovedFromMisskey": "Misskeyから削除",
}

ROUTE_PATTERN = re.compile(
    r"""Route\(\s*(?:method=)?["'](?:GET|POST)["'],\s*(?:path=)?["']/api(/[^"']+)["']""", re.S
)


class Change(TypedDict):
    path: str  # エンドポイントパス or スキーマ名
    status: str
    old_hash: str
    new_hash: str
    new_content: str
    diff: dict[str, list[Any]]


# --------------------------------------------------------------------------- 読み込み


def load_api(path: pathlib.Path) -> OpenAPI:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def implemented_paths() -> set[str]:
    """mipac/ 内で Route として参照されているパス(/api 抜き)を集める"""
    paths: set[str] = set()
    for file in (ROOT_PATH / "mipac").rglob("*.py"):
        paths.update(ROUTE_PATTERN.findall(file.read_text(encoding="utf-8")))
    return paths


def operation(api: OpenAPI, path: str) -> dict[str, Any]:
    """Misskey は全て POST だが、念のため最初のメソッドを取る"""
    return next(iter(api["paths"][path].values()))


def collect_refs(value: Any, acc: set[str]) -> set[str]:
    if isinstance(value, dict):
        ref = value.get("$ref")
        if isinstance(ref, str) and ref.startswith("#/components/schemas/"):
            acc.add(ref.rsplit("/", 1)[-1])
        for v in value.values():
            collect_refs(v, acc)
    elif isinstance(value, list):
        for v in value:
            collect_refs(v, acc)
    return acc


def referenced_schemas(api: OpenAPI, paths: set[str]) -> set[str]:
    """実装済みエンドポイントから($ref を辿って)到達できるスキーマ名"""
    schemas = api["components"]["schemas"]
    pending = set()
    for path in paths:
        if path in api["paths"]:
            collect_refs(operation(api, path), pending)
    seen: set[str] = set()
    while pending:
        name = pending.pop()
        if name in seen or name not in schemas:
            continue
        seen.add(name)
        collect_refs(schemas[name], pending)
    return seen


# --------------------------------------------------------------------------- 差分


def _hash(data: Any) -> str:
    canonical = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _value_repr(val: Any) -> str:
    if val is None:
        return "null"
    if isinstance(val, bool):
        return "boolean"
    if isinstance(val, int):
        return "integer"
    if isinstance(val, float):
        return "number"
    if isinstance(val, str):
        return val if len(val) <= 60 else f"{val[:50]}..."
    if isinstance(val, list):
        return f"array[{len(val)}]"
    if isinstance(val, dict):
        return "object"
    return type(val).__name__


def _extract_schema_name(ref: Any) -> Any:
    if isinstance(ref, str) and ref.startswith("#/components/schemas/"):
        return ref.rsplit("/", 1)[-1]
    return ref


def _format_diff_path(path: str, value: Any = None) -> str:
    """技術的なパスを読みやすくする

    200.content.application/json.schema.items.$ref
    → responses[200] › schema.items › $ref → User
    """
    formatted: list[str] = []
    for part in path.split("."):
        if part.isdigit() and len(part) == 3:
            formatted.append(f"responses[{part}]")
        elif "/" in part:
            continue  # content type は冗長なので省略
        elif part == "$ref" and value is not None:
            formatted.append(f"$ref → {_extract_schema_name(value)}")
        else:
            formatted.append(part)
    return " › ".join(p for p in formatted if p)


def _compute_json_diff(old_val: Any, new_val: Any, path: str = "") -> dict[str, list[Any]]:
    """2つの JSON 構造を比較し added / removed / type_changes / array_changes を返す"""
    result: dict[str, list[Any]] = {
        "added": [],
        "removed": [],
        "type_changes": [],
        "array_changes": [],
    }

    def _join(base: str, key: str) -> str:
        return f"{base}.{key}" if base else key

    def _is_leaf(val: Any) -> bool:
        return not isinstance(val, (dict, list)) or (
            isinstance(val, dict) and "$ref" in val and len(val) == 1
        )

    if isinstance(old_val, dict) and isinstance(new_val, dict):
        for key in old_val.keys() - new_val.keys():
            val = old_val[key]
            result["removed"].append(
                {"path": _join(path, key), "value": val if _is_leaf(val) else None}
            )
        for key in new_val.keys() - old_val.keys():
            val = new_val[key]
            result["added"].append(
                {"path": _join(path, key), "value": val if _is_leaf(val) else None}
            )
        for key in old_val.keys() & new_val.keys():
            sub = _compute_json_diff(old_val[key], new_val[key], _join(path, key))
            for k in result:
                result[k].extend(sub[k])
    elif isinstance(old_val, list) and isinstance(new_val, list):
        if old_val != new_val:
            if all(not isinstance(v, (dict, list)) for v in old_val + new_val):
                result["array_changes"].append(
                    {
                        "path": path or "(root)",
                        "added": sorted(set(new_val) - set(old_val), key=str),
                        "removed": sorted(set(old_val) - set(new_val), key=str),
                        "old_values": old_val,
                        "new_values": new_val,
                    }
                )
            else:
                result["type_changes"].append(
                    {
                        "path": path or "(root)",
                        "old": _value_repr(old_val),
                        "new": _value_repr(new_val),
                    }
                )
    else:
        old_repr, new_repr = _value_repr(old_val), _value_repr(new_val)
        if old_repr != new_repr:
            result["type_changes"].append(
                {
                    "path": path or "(root)",
                    "old": _extract_schema_name(old_val) if isinstance(old_val, str) else old_repr,
                    "new": _extract_schema_name(new_val) if isinstance(new_val, str) else new_repr,
                }
            )
    return result


def _diff_lines(diff: dict[str, list[Any]]) -> list[str]:
    """ターミナル要約用の 1 行表現"""
    lines = [f"  + {_format_diff_path(i['path'], i.get('value'))}" for i in diff["added"]]
    lines += [f"  - {_format_diff_path(i['path'], i.get('value'))}" for i in diff["removed"]]
    lines += [
        f"  ~ {_format_diff_path(tc['path'])}: {tc['old']} -> {tc['new']}"
        for tc in diff["type_changes"]
    ]
    for ac in diff["array_changes"]:
        if ac["added"] or ac["removed"]:
            parts = [f"+{v}" for v in ac["added"]] + [f"-{v}" for v in ac["removed"]]
            lines.append(f"  ~ {_format_diff_path(ac['path'])}: {' '.join(parts)}")
    return lines


def _change(name: str, status: str, old: Any, new: Any) -> Change:
    return {
        "path": name,
        "status": status,
        "old_hash": _hash(old),
        "new_hash": _hash(new),
        "new_content": json.dumps(new, ensure_ascii=False, indent=2),
        "diff": _compute_json_diff(old, new),
    }


# --------------------------------------------------------------------------- 対応状況


class Report(TypedDict):
    endpoint_status: dict[str, STATUS]  # 新 API に存在するパス
    removed_endpoints: list[str]  # 実装済みだが新 API に無いパス
    added_endpoints: list[str]  # 新 API で増えたパス
    request_body_changes: list[Change]
    response_changes: list[Change]
    schema_status: dict[str, STATUS]
    schema_changes: list[Change]


def build_report(old_api: OpenAPI, new_api: OpenAPI, implemented: set[str]) -> Report:
    report: Report = {
        "endpoint_status": {},
        "removed_endpoints": sorted(p for p in implemented if p not in new_api["paths"]),
        "added_endpoints": sorted(p for p in new_api["paths"] if p not in old_api["paths"]),
        "request_body_changes": [],
        "response_changes": [],
        "schema_status": {},
        "schema_changes": [],
    }
    for path in new_api["paths"]:
        if path not in implemented:
            report["endpoint_status"][path] = "notSupported"
            continue
        status: STATUS = "supported"
        if path in old_api["paths"]:
            old_op, new_op = operation(old_api, path), operation(new_api, path)
            for key, bucket in (
                ("requestBody", "request_body_changes"),
                ("responses", "response_changes"),
            ):
                old_part, new_part = old_op.get(key, {}), new_op.get(key, {})
                if old_part != new_part:
                    status = "needToWork"
                    report[bucket].append(_change(path, status, old_part, new_part))
        report["endpoint_status"][path] = status

    referenced = referenced_schemas(new_api, implemented)
    old_schemas, new_schemas = old_api["components"]["schemas"], new_api["components"]["schemas"]
    for name, schema in new_schemas.items():
        if name not in referenced:
            report["schema_status"][name] = "notSupported"
            continue
        old_schema = old_schemas.get(name, {})
        if old_schema == schema:
            report["schema_status"][name] = "supported"
        else:
            report["schema_status"][name] = "needToWork"
            report["schema_changes"].append(_change(name, "needToWork", old_schema, schema))
    return report


# --------------------------------------------------------------------------- 生成物


def write_endpoints_type(api: OpenAPI) -> None:
    paths = [f"/api{p}" for p in api["paths"]]
    content = (
        '"""\n=======================\n        WARNING\n=======================\n'
        " This file is automatically generated by compiler/update_api_status.py.\n"
        ' If this file is modified and then auto-generated, the changes will be lost.\n"""\n\n'
        "from typing import Literal\n\n"
        f"ENDPOINTS = Literal{json.dumps(paths, ensure_ascii=False, indent=4)}\n"
    )
    (ROOT_PATH / "mipac/types/endpoints.py").write_text(content, encoding="utf-8")


def _error_name_to_hump(name: str) -> str:
    return "".join(i.capitalize() for i in name.split("_"))


def write_errors(api: OpenAPI) -> None:
    error_map: dict[str, str] = {}
    for path in api["paths"]:
        for status_code, res in operation(api, path).get("responses", {}).items():
            if status_code == "200":
                continue
            for content in res.get("content", {}).values():
                if content.get("schema", {}).get("$ref") != "#/components/schemas/Error":
                    continue
                for example in content.get("examples", {}).values():
                    error = example["value"]["error"]
                    error_map[error["code"]] = error["message"]
    errors = sorted(error_map.items())
    with open(DATAS_PATH / "errors.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["code", "message"])
        writer.writerows(errors)
    classes = [
        f'class {_error_name_to_hump(code)}Error(APIError):\n    """{message}"""\n'
        for code, message in errors
    ]
    (ROOT_PATH / "mipac/errors/errors.py").write_text(
        "from .base import APIError\n\n\n" + "\n\n".join(classes), encoding="utf-8"
    )


def _checklist(names: list[str], status: dict[str, str]) -> str:
    lines = []
    for name in names:
        affix = " (Need to work)" if status[name] == "needToWork" else ""
        lines.append(f"- [{'x' if status[name] == 'supported' else ' '}] {name}{affix}")
    return "\n".join(lines) or "💯"


def write_support_status(api: OpenAPI, report: Report) -> None:
    es, ss = report["endpoint_status"], report["schema_status"]
    by = lambda d, s: sorted(k for k, v in d.items() if v == s)  # noqa: E731
    implemented = len(es) - len(by(es, "notSupported"))
    content = f"""# Supported Misskey Information

## Supported Misskey Version

`{api["info"]["version"]}`

## Supported endpoints ({implemented}/{len(es)})

{_checklist(by(es, "supported"), es)}

## Not supported endpoints

{_checklist(by(es, "notSupported"), es)}

## Changed request body or responses

{_checklist(by(es, "needToWork"), es)}

## Removed from Misskey

{chr(10).join(f"- {p}" for p in report["removed_endpoints"]) or "💯"}

## Supported schemas

{_checklist(sorted(ss), ss)}
"""
    (DATAS_PATH / "support_status.md").write_text(content, encoding="utf-8")


def _prepare_diff_for_template(diff: dict[str, list[Any]]) -> dict[str, Any] | None:
    if not any(diff.values()):
        return None
    max_items = 30
    result: dict[str, Any] = {}
    if diff["array_changes"]:
        result["array_changes"] = [
            {
                "path_display": _format_diff_path(ac["path"]),
                "added_display": ", ".join(map(str, ac["added"])),
                "removed_display": ", ".join(map(str, ac["removed"])),
                "old_values_display": ", ".join(map(str, ac["old_values"])),
                "new_values_display": ", ".join(map(str, ac["new_values"])),
                "added": bool(ac["added"]),
                "removed": bool(ac["removed"]),
            }
            for ac in diff["array_changes"][:max_items]
        ]
    for key in ("added", "removed"):
        if diff[key]:
            result[key] = [
                _format_diff_path(i["path"], i.get("value")) for i in diff[key][:max_items]
            ]
    if diff["type_changes"]:
        result["type_changes"] = [
            {"path": _format_diff_path(tc["path"]), "old": tc["old"], "new": tc["new"]}
            for tc in diff["type_changes"][:max_items]
        ]
    return result


def _prepare_section_items(changes: list[Change]) -> list[dict[str, Any]]:
    return [
        {
            "path_or_name": c["path"],
            "status": c["status"],
            "status_label": STATUS_LABELS.get(c["status"], c["status"]),
            "old_hash": c["old_hash"],
            "new_hash": c["new_hash"],
            "diff": _prepare_diff_for_template(c["diff"]),
            "new_content": c["new_content"],
        }
        for c in changes
    ]


def write_html_report(api: OpenAPI, report: Report) -> None:
    es, ss = report["endpoint_status"], report["schema_status"]
    by = lambda d, s: sorted(k for k, v in d.items() if v == s)  # noqa: E731
    support_status = {
        "stats": {
            "total_endpoints": len(es),
            "implemented_endpoints": len(by(es, "supported")) + len(by(es, "needToWork")),
            "supported_endpoints": len(by(es, "supported")),
            "need_to_work_endpoints": len(by(es, "needToWork")),
            "not_supported_endpoints": len(by(es, "notSupported")),
            "removed_endpoints": len(report["removed_endpoints"]),
            "total_schemas": len(ss),
            "implemented_schemas": len(by(ss, "supported")) + len(by(ss, "needToWork")),
        },
        "supported_endpoints": by(es, "supported"),
        "need_to_work_endpoints": by(es, "needToWork"),
        "not_supported_endpoints": by(es, "notSupported"),
        "removed_endpoints": report["removed_endpoints"],
        "schema_supported": by(ss, "supported"),
        "schema_need_to_work": by(ss, "needToWork"),
        "schema_not_supported": by(ss, "notSupported"),
    }
    sections = [
        {
            "title": "📥 リクエストボディの変更",
            "items": _prepare_section_items(report["request_body_changes"]),
        },
        {
            "title": "📤 レスポンスの変更",
            "items": _prepare_section_items(report["response_changes"]),
        },
        {"title": "📋 スキーマの変更", "items": _prepare_section_items(report["schema_changes"])},
    ]
    env = Environment(
        loader=FileSystemLoader(str(COMPILER_PATH / "templates")),
        autoescape=select_autoescape(("html", "xml")),
    )
    html = env.get_template("api_changes_report.html.j2").render(
        api_version=api["info"]["version"],
        has_changes=any(s["items"] for s in sections),
        sections=sections,
        support_status=support_status,
    )
    (DATAS_PATH / "api_changes_report.html").write_text(html, encoding="utf-8")


def print_summary(old_api: OpenAPI, new_api: OpenAPI, report: Report) -> None:
    es = report["endpoint_status"]
    counts = {
        s: sum(1 for v in es.values() if v == s)
        for s in ("supported", "needToWork", "notSupported")
    }
    print(f"Misskey {old_api['info']['version']} -> {new_api['info']['version']}")
    print(
        f"endpoints: {len(es)} total / implemented {counts['supported'] + counts['needToWork']}"
        f" (supported {counts['supported']}, needToWork {counts['needToWork']})"
        f" / not implemented {counts['notSupported']}"
    )
    print(f"added endpoints: {len(report['added_endpoints'])}")
    for path in report["added_endpoints"]:
        print(f"  + {path}")
    print(f"removed endpoints still used by MiPAC: {len(report['removed_endpoints'])}")
    for path in report["removed_endpoints"]:
        print(f"  - {path}")
    for title, changes in (
        ("REQUEST", report["request_body_changes"]),
        ("RESPONSES", report["response_changes"]),
        ("SCHEMA", report["schema_changes"]),
    ):
        for change in changes:
            print(f"[CHANGED: {title}] {change['path']}")
            print("\n".join(_diff_lines(change["diff"])))


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("new_api", nargs="?", type=pathlib.Path, help="新しい OpenAPI JSON")
    args = parser.parse_args()

    old_api = load_api(API_PATH)
    new_api = load_api(args.new_api) if args.new_api else old_api
    report = build_report(old_api, new_api, implemented_paths())

    write_endpoints_type(new_api)
    write_errors(new_api)
    write_support_status(new_api, report)
    write_html_report(new_api, report)
    if args.new_api and args.new_api.resolve() != API_PATH.resolve():
        shutil.copyfile(args.new_api, API_PATH)
    print_summary(old_api, new_api, report)


if __name__ == "__main__":
    main()
