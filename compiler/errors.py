import csv
import json

from type import OpenAPI

pre = """from .base import APIError


"""
template = """class %sError(APIError):
    \"\"\"%s\"\"\"
"""


def error_name_to_hump(name: str) -> str:
    return "".join([i.capitalize() for i in name.split("_")])


def gen_errors_py_files():
    error_list = {}
    with open("datas/errors.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for idx, row in enumerate(reader):
            if idx == 0:
                continue
            if row:
                error_list[row[0]] = row[1]

    all_content = [template % (error_name_to_hump(i), value) for i, value in error_list.items()]

    with open("../mipac/errors/errors.py", "w", encoding="utf-8") as f:
        f.write(pre + "\n\n".join(all_content))


def gen_errors_csv():
    with open("datas/v13_api.json", mode="r", encoding="utf-8") as f:
        api: OpenAPI = json.load(f)
    error_map = {}
    for path_value in api["paths"].values():
        for method_value in path_value.values():
            for status_code, res_value in method_value["responses"].items():
                if status_code == "200":
                    continue
                if "content" not in res_value:
                    continue
                for content_value in res_value["content"].values():
                    if content_value.get("schema", {}).get("$ref") != "#/components/schemas/Error":
                        continue
                    for error_value in content_value["examples"].values():
                        error_data = error_value["value"]["error"]
                        code = error_data["code"]
                        message = error_data["message"]
                        error_map[code] = message
    sorted_error_map = sorted(error_map.items())
    with open("datas/errors.csv", "w", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["code", "message"])
        for error in sorted_error_map:
            writer.writerow(error)


if __name__ == "__main__":
    gen_errors_csv()
    gen_errors_py_files()
    print("Done")
