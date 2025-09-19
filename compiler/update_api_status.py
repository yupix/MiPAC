import copy
import hashlib
import json
import pathlib
import sys

from type import OpenAPI, OpenAPIComponentSchema, OpenAPIRequestBody
from typing import Any, Literal, TypedDict

import tqdm

CURRENT_PATH = sys.path[0]
if CURRENT_PATH.endswith("compiler"):
    CURRENT_PATH = CURRENT_PATH[:-9]

COMPILER_PATH = pathlib.Path(CURRENT_PATH).joinpath("compiler").as_posix()

sys.path.append(CURRENT_PATH)

from mipac.utils.util import COLORS  # noqa: E402

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


def get_sha256_hash(data: dict[str, Any] | OpenAPIComponentSchema | OpenAPIRequestBody):
    return hashlib.sha256(
        json.dumps(data, ensure_ascii=False, indent=0).encode("utf-8")
    ).hexdigest()


"""
support: Misskeyに実装されており、実装する予定があるまたは実装されている
removed: MiPACでサポートされているが、Misskeyから削除された
"""
SECTIONS = Literal["support", "removed"]

with open(f"{COMPILER_PATH}/datas/v13_api.json", mode="r", encoding="utf-8") as f:
    api: OpenAPI = json.load(f)

with open(f"{COMPILER_PATH}/datas/endpoints.json", mode="r", encoding="utf-8") as f:
    endpoints: IData = json.load(f)
    _endpoints: IData = copy.deepcopy(endpoints)

# パスに関する情報を更新する
for path in tqdm.tqdm(api["paths"]):
    old_data = endpoints["endpoints"]["support"].get(path, None)
    current_request_body_hash = get_sha256_hash(api["paths"][path]["post"].get("requestBody", {}))
    current_response_body_hash = get_sha256_hash(api["paths"][path]["post"].get("responses", {}))
    if old_data is None:
        endpoints["endpoints"]["support"][path] = {
            "path": path,
            "status": "notSupported",
            "request_body_hash": get_sha256_hash(
                api["paths"][path]["post"].get("requestBody", {})
            ),
            "response_body_hash": get_sha256_hash(api["paths"][path]["post"].get("responses", {})),
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
            endpoints["endpoints"]["support"][path][
                "request_body_hash"
            ] = current_request_body_hash
        if current_response_body_hash != old_data["response_body_hash"]:
            print(
                f"{COLORS.green}[CHANGED: RESPONSES] changed responses hash {COLORS.reset} {path} {COLORS.reset}"
            )
            endpoints["endpoints"]["support"][path][
                "response_body_hash"
            ] = current_response_body_hash


# Misskeyから削除されたエンドポイントをremovedに移動する
for path in tqdm.tqdm(_endpoints["endpoints"]["support"]):
    endpoints["endpoints"]["removed"][path] = _endpoints["endpoints"]["support"][path]
    # Misskeyから削除された場合はRemovedFromMisskeyにする
    endpoints["endpoints"]["removed"][path]["status"] = "RemovedFromMisskey"
    del endpoints["endpoints"]["support"][path]

# MiPACからの削除が完了した場合はremovedから削除する
for path in tqdm.tqdm(_endpoints["endpoints"]["removed"]):
    if endpoints["endpoints"]["removed"][path]["status"] == "Removed":
        del endpoints["endpoints"]["removed"][path]
        continue

# スキーマに関する情報を更新する
for schema in tqdm.tqdm(api["components"]["schemas"]):
    try:
        del _endpoints["schemas"][schema]
    except KeyError:
        pass

    old_data = endpoints["schemas"].get(schema, None)
    if old_data is None:
        endpoints["schemas"][schema] = {
            "name": schema,
            "hash": get_sha256_hash(api["components"]["schemas"][schema]),
            "status": "notSupported",
        }
    else:
        current_hash = get_sha256_hash(api["components"]["schemas"][schema])
        if current_hash != old_data["hash"]:
            print(
                f"{COLORS.green}[CHANGED: SCHEMA] changed schema hash {COLORS.reset} {schema} {COLORS.reset}"
            )
            endpoints["schemas"][schema]["hash"] = current_hash

            if (
                endpoints["schemas"][schema]["status"] == "supported"
            ):  # サポート済みの場合のみステータスを変更する
                endpoints["schemas"][schema]["status"] = "needToWork"


with open(f"{COMPILER_PATH}/datas/endpoints.json", mode="w", encoding="utf-8") as f:
    json.dump(endpoints, f, ensure_ascii=False, indent=4)


def get_list(data: IData, section: SECTIONS, status: STATUS):
    result = ""
    for path_name in data["endpoints"][section]:
        path = data["endpoints"][section][path_name]
        if path["status"] == status:
            affix = "(Need to work)" if path["status"] == "needToWork" else ""
            result += f"- [{'x' if path['status'] == 'supported' else ' '}] {path['path']}{f' {affix}' if affix else ''}\n"
    return result


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

print("done")
