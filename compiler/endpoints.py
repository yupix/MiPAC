import json

from type import OpenAPI

PATHS: list[str] = []
PREFIX = '/api'
IMPORTS = "from typing import Literal\n\n"
TEMPLATES = "ENDPOINTS = "

with open('./datas/v13_api.json') as f:
    api: OpenAPI = json.load(f)
    for path in api['paths']:
        PATHS.append(f'{PREFIX}{path}')

with open('./datas/ayuskey_api.json') as f:
    api: OpenAPI = json.load(f)
    for path in api['paths']:
        PATHS.append(f'{PREFIX}{path}')

with open('../mipac/types/endpoints.py', 'w', encoding='utf-8') as f:
    data = json.dumps(list(dict.fromkeys(PATHS)), ensure_ascii=False, indent=4)
    f.write(
        f'{IMPORTS}{TEMPLATES}Literal{data}'
    )
