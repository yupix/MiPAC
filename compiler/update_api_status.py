import copy
import hashlib
import html
import json
import pathlib
import sys

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError:
    raise ImportError(
        "Jinja2 が必要です。インストール: pip install jinja2"
    ) from None

from type import OpenAPI, OpenAPIComponentSchema, OpenAPIRequestBody
from typing import Any, Literal, TypedDict

try:
    import tqdm
    progress = tqdm.tqdm
except ImportError:
    progress = lambda x: x  # noqa: E731

CURRENT_PATH = sys.path[0]
if CURRENT_PATH.endswith("compiler"):
    CURRENT_PATH = CURRENT_PATH[:-9]

COMPILER_PATH = pathlib.Path(CURRENT_PATH).joinpath("compiler").as_posix()

sys.path.append(CURRENT_PATH)

try:
    from mipac.utils.util import COLORS  # noqa: E402
except ImportError:
    COLORS = type("Colors", (), {"green": "", "reset": ""})()

"""
notSupported: MiPACに実装されていない
supported: MiPACでサポートされている
needToWork: サポートされているが、作業が必要
RemovedFromMisskey: Misskeyから削除された
Removed: MiPACから削除された（これに変更するとremovedから自動で削除されます）
"""

STATUS = Literal["notSupported", "supported", "needToWork", "RemovedFromMisskey", "Removed"]


class IEndpoint(TypedDict):
    path: str
    status: STATUS
    request_body_hash: str | None
    response_body_hash: str | None


class ISchema(TypedDict):
    name: str
    hash: str
    status: STATUS


class IData(TypedDict):
    endpoints: dict[Literal["support", "removed"], dict[str, IEndpoint]]
    schemas: dict[str, ISchema]


def _canonical_json(data: dict[str, Any] | OpenAPIComponentSchema | OpenAPIRequestBody) -> str:
    """キー順・フォーマットに依存しない正規化されたJSON文字列を生成する"""
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def get_sha256_hash(data: dict[str, Any] | OpenAPIComponentSchema | OpenAPIRequestBody) -> str:
    """キー順やフォーマットの違いに影響されないハッシュを生成する"""
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()


def _value_repr(val: Any) -> str:
    """型・値の簡潔な表現を返す（差分表示用）"""
    if val is None:
        return "null"
    if isinstance(val, bool):
        return "boolean"
    if isinstance(val, int):
        return "integer"
    if isinstance(val, float):
        return "number"
    if isinstance(val, str):
        # スキーマの型名（string, integer等）や短い文字列はそのまま
        if len(val) <= 60 and val not in ("", " "):
            return val
        return f"{val[:50]}..." if len(val) > 50 else val
    if isinstance(val, list):
        return f"array[{len(val)}]"
    if isinstance(val, dict):
        return "object"
    return str(type(val).__name__)


def _extract_schema_name(ref: str) -> str:
    """$ref からスキーマ名を抽出。例: #/components/schemas/User → User"""
    if not isinstance(ref, str) or not ref.startswith("#/components/schemas/"):
        return ref
    return ref.split("/")[-1]


def _format_diff_path(path: str, value: Any = None) -> str:
    """
    技術的なパスを人間が読みやすい形式に変換。
    例: 200.content.application/json.schema.items.$ref → responses[200] › schema.items › $ref → User
    """
    parts = path.split(".")
    formatted: list[str] = []
    for i, part in enumerate(parts):
        if part.isdigit() and len(part) == 3:
            # HTTP ステータスコード
            formatted.append(f"responses[{part}]")
        elif "/" in part:
            # content type (application/json 等) は省略（冗長なため）
            continue
        elif part == "$ref" and value is not None:
            schema_name = _extract_schema_name(value) if isinstance(value, str) else value
            formatted.append(f"$ref → {schema_name}")
        else:
            formatted.append(part)
    return " › ".join(p for p in formatted if p)


def _compute_json_diff(
    old_val: Any, new_val: Any, path: str = ""
) -> dict[str, list[Any]]:
    """
    2つのJSON構造を比較し、追加・削除・型変更を検出する。
    戻り値: {"added": [...], "removed": [...], "type_changes": [...]}
    added/removed は {path, value} の形式で、参照先などが分かるようにする
    """
    result: dict[str, list[Any]] = {
        "added": [],
        "removed": [],
        "type_changes": [],
        "array_changes": [],
    }

    def _join_path(base: str, key: str) -> str:
        return f"{base}.{key}" if base else key

    def _is_leaf(val: Any) -> bool:
        return not isinstance(val, (dict, list)) or (
            isinstance(val, dict) and "$ref" in val and len(val) == 1
        )

    if isinstance(old_val, dict) and isinstance(new_val, dict):
        old_keys = set(old_val.keys())
        new_keys = set(new_val.keys())

        for key in old_keys - new_keys:
            val = old_val[key]
            full_path = _join_path(path, key)
            if key == "$ref" and isinstance(val, str):
                result["removed"].append({"path": full_path, "value": val})
            elif _is_leaf(val):
                result["removed"].append({"path": full_path, "value": val})
            else:
                result["removed"].append({"path": full_path, "value": None})

        for key in new_keys - old_keys:
            val = new_val[key]
            full_path = _join_path(path, key)
            if key == "$ref" and isinstance(val, str):
                result["added"].append({"path": full_path, "value": val})
            elif _is_leaf(val):
                result["added"].append({"path": full_path, "value": val})
            else:
                result["added"].append({"path": full_path, "value": None})

        for key in old_keys & new_keys:
            sub_path = _join_path(path, key)
            sub_old = old_val[key]
            sub_new = new_val[key]
            sub_result = _compute_json_diff(sub_old, sub_new, sub_path)
            result["added"].extend(sub_result["added"])
            result["removed"].extend(sub_result["removed"])
            result["type_changes"].extend(sub_result["type_changes"])
            result["array_changes"].extend(sub_result.get("array_changes", []))
    elif isinstance(old_val, list) and isinstance(new_val, list):
        if old_val != new_val:
            # 配列の差分を具体的に表示（required 等の文字列配列向け）
            array_diff_done = False
            try:
                if all(not isinstance(v, (dict, list)) for v in old_val + new_val):
                    old_set = set(old_val)
                    new_set = set(new_val)
                    added_items = sorted(new_set - old_set, key=str)
                    removed_items = sorted(old_set - new_set, key=str)
                    # 追加・削除がなくても enum 等は全文表示するため array_changes に含める
                    if added_items or removed_items or old_val != new_val:
                        result["array_changes"].append({
                            "path": path or "(root)",
                            "added": added_items,
                            "removed": removed_items,
                            "old_values": old_val,  # 全文表示用（enum等）
                            "new_values": new_val,
                        })
                    array_diff_done = True
            except (TypeError, ValueError):
                pass
            if not array_diff_done:
                result["type_changes"].append({
                    "path": path or "(root)",
                    "old": _value_repr(old_val),
                    "new": _value_repr(new_val),
                })
    else:
        old_repr = _value_repr(old_val)
        new_repr = _value_repr(new_val)
        if old_repr != new_repr:
            # $ref の場合は参照先スキーマ名を表示
            old_display = _extract_schema_name(old_val) if isinstance(old_val, str) and old_val.startswith("#/") else old_repr
            new_display = _extract_schema_name(new_val) if isinstance(new_val, str) and new_val.startswith("#/") else new_repr
            result["type_changes"].append({
                "path": path or "(root)",
                "old": old_display,
                "new": new_display,
            })

    return result


"""
support: Misskeyに実装されており、実装する予定があるまたは実装されている
removed: MiPACでサポートされているが、Misskeyから削除された
"""
SECTIONS = Literal["support", "removed"]

# 変更検知用のレポートデータ
ChangeReport = TypedDict(
    "ChangeReport",
    {
        "request_body_changes": list[dict[str, Any]],
        "response_changes": list[dict[str, Any]],
        "schema_changes": list[dict[str, Any]],
    },
)
change_report: ChangeReport = {
    "request_body_changes": [],
    "response_changes": [],
    "schema_changes": [],
}

with open(f"{COMPILER_PATH}/datas/v13_api.json", mode="r", encoding="utf-8") as f:
    api: OpenAPI = json.load(f)

# 前回のAPIスナップショット（差分表示用）
api_previous: OpenAPI | None = None
_api_previous_path = pathlib.Path(f"{COMPILER_PATH}/datas/v13_api_previous.json")
if _api_previous_path.exists():
    with open(_api_previous_path, mode="r", encoding="utf-8") as f:
        api_previous = json.load(f)

with open(f"{COMPILER_PATH}/datas/endpoints.json", mode="r", encoding="utf-8") as f:
    endpoints: IData = json.load(f)
    _endpoints: IData = copy.deepcopy(endpoints)

# パスに関する情報を更新する
for path in progress(api["paths"]):
    old_data = endpoints["endpoints"]["support"].get(path, None)
    current_request_body = api["paths"][path]["post"].get("requestBody", {})
    current_responses = api["paths"][path]["post"].get("responses", {})
    current_request_body_hash = get_sha256_hash(current_request_body)
    current_response_body_hash = get_sha256_hash(current_responses)
    if old_data is None:
        endpoints["endpoints"]["support"][path] = {
            "path": path,
            "status": "notSupported",
            "request_body_hash": current_request_body_hash,
            "response_body_hash": current_response_body_hash,
        }
    else:
        # 既存のデータから削除することで残りはremovedにする
        del _endpoints["endpoints"]["support"][path]

        if endpoints["endpoints"]["support"][path]["status"] == "supported":
            # ハッシュが変更されている場合はneedToWorkにする、ハッシュの設定前にやらないとハッシュが変更されてるか分からない
            if (
                current_request_body_hash != old_data["request_body_hash"]
                or current_response_body_hash != old_data["response_body_hash"]
            ):
                endpoints["endpoints"]["support"][path]["status"] = "needToWork"

        # ハッシュが変更されているかどうかを確認する
        if current_request_body_hash != old_data["request_body_hash"]:
            print(
                f"{COLORS.green}[CHANGED: REQUEST] changed request body hash {COLORS.reset} {path} {COLORS.reset}"
            )
            endpoints["endpoints"]["support"][path]["request_body_hash"] = current_request_body_hash
            old_request_body = {}
            if api_previous and path in api_previous.get("paths", {}):
                old_request_body = api_previous["paths"][path].get("post", {}).get("requestBody", {})
            diff = _compute_json_diff(old_request_body, current_request_body)
            change_report["request_body_changes"].append(
                {
                    "path": path,
                    "status": endpoints["endpoints"]["support"][path]["status"],
                    "old_hash": old_data["request_body_hash"],
                    "new_hash": current_request_body_hash,
                    "new_content": json.dumps(current_request_body, ensure_ascii=False, indent=2),
                    "diff": diff,
                }
            )
        if current_response_body_hash != old_data["response_body_hash"]:
            print(
                f"{COLORS.green}[CHANGED: RESPONSES] changed responses hash {COLORS.reset} {path} {COLORS.reset}"
            )
            endpoints["endpoints"]["support"][path]["response_body_hash"] = current_response_body_hash
            old_responses = {}
            if api_previous and path in api_previous.get("paths", {}):
                old_responses = api_previous["paths"][path].get("post", {}).get("responses", {})
            diff = _compute_json_diff(old_responses, current_responses)
            change_report["response_changes"].append(
                {
                    "path": path,
                    "status": endpoints["endpoints"]["support"][path]["status"],
                    "old_hash": old_data["response_body_hash"],
                    "new_hash": current_response_body_hash,
                    "new_content": json.dumps(current_responses, ensure_ascii=False, indent=2),
                    "diff": diff,
                }
            )


# Misskeyから削除されたエンドポイントをremovedに移動する
for path in progress(_endpoints["endpoints"]["support"]):
    endpoints["endpoints"]["removed"][path] = _endpoints["endpoints"]["support"][path]
    # Misskeyから削除された場合はRemovedFromMisskeyにする
    endpoints["endpoints"]["removed"][path]["status"] = "RemovedFromMisskey"
    del endpoints["endpoints"]["support"][path]

# MiPACからの削除が完了した場合はremovedから削除する
for path in progress(_endpoints["endpoints"]["removed"]):
    if endpoints["endpoints"]["removed"][path]["status"] == "Removed":
        del endpoints["endpoints"]["removed"][path]
        continue

# スキーマに関する情報を更新する
for schema in progress(api["components"]["schemas"]):
    try:
        del _endpoints["schemas"][schema]
    except KeyError:
        pass

    old_data = endpoints["schemas"].get(schema, None)
    current_schema = api["components"]["schemas"][schema]
    if old_data is None:
        endpoints["schemas"][schema] = {
            "name": schema,
            "hash": get_sha256_hash(current_schema),
            "status": "notSupported",
        }
    else:
        current_hash = get_sha256_hash(current_schema)
        if current_hash != old_data["hash"]:
            print(
                f"{COLORS.green}[CHANGED: SCHEMA] changed schema hash {COLORS.reset} {schema} {COLORS.reset}"
            )
            endpoints["schemas"][schema]["hash"] = current_hash

            if endpoints["schemas"][schema]["status"] == "supported":
                # サポート済みの場合のみステータスを変更する
                endpoints["schemas"][schema]["status"] = "needToWork"

            old_schema = {}
            if api_previous:
                old_schema = api_previous.get("components", {}).get("schemas", {}).get(schema, {})
            diff = _compute_json_diff(old_schema, current_schema)
            change_report["schema_changes"].append(
                {
                    "name": schema,
                    "status": endpoints["schemas"][schema]["status"],
                    "old_hash": old_data["hash"],
                    "new_hash": current_hash,
                    "new_content": json.dumps(current_schema, ensure_ascii=False, indent=2),
                    "diff": diff,
                }
            )


def get_list(data: IData, section: SECTIONS, status: STATUS):
    result = ""
    for path_name in data["endpoints"][section]:
        path = data["endpoints"][section][path_name]
        if path["status"] == status:
            affix = "(Need to work)" if path["status"] == "needToWork" else ""
            result += f"- [{'x' if path['status'] == 'supported' else ' '}] {path['path']}{f' {affix}' if affix else ''}\n"
    return result


def _escape_html(text: str) -> str:
    return html.escape(text)


def _prepare_diff_for_template(diff: dict[str, list] | None) -> dict[str, Any] | None:
    """テンプレート用に差分データを整形する"""
    if not diff or not (
        diff.get("added")
        or diff.get("removed")
        or diff.get("type_changes")
        or diff.get("array_changes")
    ):
        return None
    max_items = 30
    max_array_items = 15
    result: dict[str, Any] = {}
    if diff.get("array_changes"):
        result["array_changes"] = []
        for ac in diff["array_changes"][:max_items]:
            added = ac.get("added", [])[:max_array_items]
            removed = ac.get("removed", [])[:max_array_items]
            added_extra = f" 他{len(ac.get('added', [])) - max_array_items}件" if len(ac.get("added", [])) > max_array_items else ""
            removed_extra = f" 他{len(ac.get('removed', [])) - max_array_items}件" if len(ac.get("removed", [])) > max_array_items else ""
            old_vals = ac.get("old_values", [])
            new_vals = ac.get("new_values", [])
            old_values_display = ", ".join(str(v) for v in old_vals) if old_vals else ""
            new_values_display = ", ".join(str(v) for v in new_vals) if new_vals else ""
            result["array_changes"].append({
                "path_display": _format_diff_path(ac["path"]),
                "added_display": ", ".join(str(a) for a in added) + added_extra if added else "",
                "removed_display": ", ".join(str(r) for r in removed) + removed_extra if removed else "",
                "old_values_display": old_values_display,
                "new_values_display": new_values_display,
                "added": bool(added),
                "removed": bool(removed),
            })
    if diff.get("added"):
        items = diff["added"][:max_items]
        result["added"] = [_format_diff_path(i["path"], i.get("value")) if isinstance(i, dict) else _format_diff_path(i) for i in items]
    if diff.get("removed"):
        items = diff["removed"][:max_items]
        result["removed"] = [_format_diff_path(i["path"], i.get("value")) if isinstance(i, dict) else _format_diff_path(i) for i in items]
    if diff.get("type_changes"):
        result["type_changes"] = [
            {"path": _format_diff_path(tc["path"]), "old": tc["old"], "new": tc["new"]}
            for tc in diff["type_changes"][:max_items]
        ]
    return result


STATUS_LABELS: dict[str, str] = {
    "supported": "完全対応",
    "needToWork": "要作業",
    "notSupported": "未対応",
    "RemovedFromMisskey": "Misskeyから削除",
    "Removed": "削除済み",
}


def _prepare_section_items(
    raw_items: list[dict], type_label: str
) -> list[dict[str, Any]]:
    """セクションのアイテムをテンプレート用に整形"""
    return [
        {
            "path_or_name": item.get("path", item.get("name", "")),
            "status": item.get("status", ""),
            "status_label": STATUS_LABELS.get(item.get("status", ""), item.get("status", "")),
            "old_hash": (item.get("old_hash") or "")[:16] + "...",
            "new_hash": (item.get("new_hash") or "")[:16] + "...",
            "diff": _prepare_diff_for_template(item.get("diff")),
            "new_content": item.get("new_content", ""),
        }
        for item in raw_items
    ]


def _prepare_support_status(endpoints_data: IData) -> dict[str, Any]:
    """サポート状況をテンプレート用に整形する"""
    support = endpoints_data["endpoints"]["support"]
    removed = endpoints_data["endpoints"]["removed"]
    schemas = endpoints_data["schemas"]

    supported = [p for p, d in support.items() if d["status"] == "supported"]
    need_to_work = [p for p, d in support.items() if d["status"] == "needToWork"]
    not_supported = [p for p, d in support.items() if d["status"] == "notSupported"]
    removed_list = [p for p, d in removed.items() if d["status"] == "RemovedFromMisskey"]

    schema_supported = [n for n, d in schemas.items() if d["status"] == "supported"]
    schema_need_to_work = [n for n, d in schemas.items() if d["status"] == "needToWork"]
    schema_not_supported = [n for n, d in schemas.items() if d["status"] == "notSupported"]

    total_endpoints = len(support)
    implemented_endpoints = len(supported) + len(need_to_work)
    total_schemas = len(schemas)
    implemented_schemas = len(schema_supported) + len(schema_need_to_work)

    return {
        "stats": {
            "total_endpoints": total_endpoints,
            "implemented_endpoints": implemented_endpoints,
            "supported_endpoints": len(supported),
            "need_to_work_endpoints": len(need_to_work),
            "not_supported_endpoints": len(not_supported),
            "removed_endpoints": len(removed_list),
            "total_schemas": total_schemas,
            "implemented_schemas": implemented_schemas,
        },
        "supported_endpoints": supported,
        "need_to_work_endpoints": need_to_work,
        "not_supported_endpoints": not_supported,
        "removed_endpoints": removed_list,
        "schema_supported": schema_supported,
        "schema_need_to_work": schema_need_to_work,
        "schema_not_supported": schema_not_supported,
    }


def _generate_html_report(
    report: ChangeReport, api_version: str, endpoints_data: IData
) -> str:
    """JinjaテンプレートでHTMLレポートを生成する"""
    has_changes = bool(
        report["request_body_changes"]
        or report["response_changes"]
        or report["schema_changes"]
    )
    sections = [
        {
            "title": "📥 リクエストボディの変更",
            "type_label": "リクエストボディ",
            "items": _prepare_section_items(report["request_body_changes"], "リクエストボディ"),
        },
        {
            "title": "📤 レスポンスの変更",
            "type_label": "レスポンス",
            "items": _prepare_section_items(report["response_changes"], "レスポンス"),
        },
        {
            "title": "📋 スキーマの変更",
            "type_label": "スキーマ",
            "items": _prepare_section_items(report["schema_changes"], "スキーマ"),
        },
    ]
    support_status = _prepare_support_status(endpoints_data)
    template_dir = pathlib.Path(COMPILER_PATH) / "templates"
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(("html", "xml")),
    )
    template = env.get_template("api_changes_report.html.j2")
    return template.render(
        api_version=api_version,
        has_changes=has_changes,
        sections=sections,
        support_status=support_status,
    )


# ファイル出力（処理失敗時は previous を上書きしない）
try:
    with open(f"{COMPILER_PATH}/datas/endpoints.json", mode="w", encoding="utf-8") as f:
        json.dump(endpoints, f, ensure_ascii=False, indent=4)

    with open(f"{COMPILER_PATH}/datas/support_status.md", mode="w", encoding="utf-8") as f:
        path_number = len(endpoints["endpoints"]["support"])
        supported_path_number = len(
            [
                path
                for path in endpoints["endpoints"]["support"]
                if endpoints["endpoints"]["support"][path]["status"] == "supported"
                or endpoints["endpoints"]["support"][path]["status"] == "needToWork"
            ]
        )
        supported_endpoints = get_list(endpoints, "support", "supported")
        not_supported_endpoints = get_list(endpoints, "support", "notSupported")
        removed_from_misskey_endpoints = get_list(endpoints, "removed", "RemovedFromMisskey")
        need_to_work_endpoints = get_list(endpoints, "support", "needToWork")
        support_schemas = ""
        for schema_name in endpoints["schemas"]:
            schema = endpoints["schemas"][schema_name]
            affix = "(Need to work)" if schema["status"] == "needToWork" else ""
            support_schemas += f"- [{'x' if schema['status'] == 'supported' else ' '}] {schema['name']}{f' {affix}' if affix else ''}\n"
        f.write(
            f"""# Supported Misskey Information

## Supported Misskey Version

`{api['info']['version']}`

## Supported endpoints ({supported_path_number}/{path_number})

{supported_endpoints}

## Not supported endpoints

{"💯" if len(not_supported_endpoints.strip()) == 0 else not_supported_endpoints[:-1]}

## Changed request body or responses

{"💯" if len(need_to_work_endpoints.strip()) == 0 else need_to_work_endpoints}

## Removed from Misskey

{"💯" if len(removed_from_misskey_endpoints.strip()) == 0 else removed_from_misskey_endpoints}

## Supported schemas

{support_schemas[:-1]}
"""
        )

    html_report = _generate_html_report(change_report, api["info"]["version"], endpoints)
    with open(f"{COMPILER_PATH}/datas/api_changes_report.html", mode="w", encoding="utf-8") as f:
        f.write(html_report)
except Exception:
    raise
else:
    # 処理がすべて成功した場合のみ previous を上書き（失敗時は既存を保持）
    with open(_api_previous_path, mode="w", encoding="utf-8") as f:
        json.dump(api, f, ensure_ascii=False, indent=2)

print("done")
