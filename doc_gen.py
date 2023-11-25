import os
import importlib
import inspect
from pathlib import PurePath
import subprocess
from typing import TypedDict


def get_defined_functions_and_classes(module):
    functions = []
    classes = []

    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and obj.__module__ == module.__name__:
            functions.append(name)
        elif inspect.isclass(obj) and obj.__module__ == module.__name__:
            classes.append(name)

    return functions, classes


class IGenerateSphinx(TypedDict):
    module_path: PurePath
    module_name: str
    functions: list[str]
    classes: list[str]


def generate_sphinx_output(data: list[IGenerateSphinx]):
    output = []
    output.append("API Reference\n===============\n")
    tmp = {}
    for i in hierarchy.values():
        tmp[i] = []
        # tmp[i].append(f"{i}\n{'-'*len(i)}")

    tmp["__OTHER"] = []

    def add_data(_data: IGenerateSphinx, add_to: list):
        if _data["functions"]:
            for function in _data["functions"]:
                add_to.append(f"\n{function}\n" + "~" * len(function))
                add_to.append(f".. autofunction:: {_data['module_name']}.{function}")

        if _data["classes"]:
            for class_name in _data["classes"]:
                add_to.append(f"\n{class_name}\n" + "~" * len(class_name))
                full_class_name = f"{_data['module_name']}.{class_name}"
                add_to.append(f".. attributetable:: {full_class_name}")
                add_to.append(f".. autoclass:: {full_class_name}\n    :members:")

    for i in data:
        add_to = "__OTHER"
        for category in hierarchy.keys():
            if PurePath(category).as_posix() in i["module_path"].as_posix():
                add_to = hierarchy[category]
        add_data(i, tmp[add_to])

    for k, v in tmp.items():
        output.append(f"{k}\n{'-'*len(k)}")
        output.append("\n\n".join(v))
    return "\n".join(output)


def generate_documentation(base_path, output_file, hierarchy, exclude_files=[]):
    documentation = []
    items: list[IGenerateSphinx] = []

    for file in [
        {"filename": file, "root": root}
        for root, dirs, files in os.walk(base_path)
        if root != "__pycache__"
        for file in files
    ]:
        if file["filename"].endswith(".py") and file["filename"] not in exclude_files:
            module_path = os.path.join(file["root"], file["filename"])
            module_import_path = module_path.replace(os.path.sep, ".").replace(".py", "")

            module = importlib.import_module(module_import_path)
            functions, classes = get_defined_functions_and_classes(module)
            if functions or classes:
                items.append(
                    {
                        "module_path": PurePath(module_path),
                        "module_name": module_import_path,
                        "functions": functions,
                        "classes": classes,
                    }
                )
    doc_content = generate_sphinx_output(items)
    documentation.append(doc_content)
    with open(output_file, "w", encoding="utf-8") as doc_file:
        doc_file.write("\n\n".join(documentation))


if __name__ == "__main__":
    hierarchy = {
        "mipac/models": "Misskey Models",
        "mipac/manager": "Managers",
        "mipac/actions": "Actions",
        "mipac/types": "Type class",
        "mipac/errors": "Errors",
    }
    source_path = "mipac"
    output_path = "docs/index.rst"
    excluded_files = ["__init__.py", "_version.py"]  # Add files to exclude here
    generate_documentation(source_path, output_path, hierarchy, exclude_files=excluded_files)
    os.chdir("./docs")
    subprocess.run(
        "make gettext && sphinx-intl update -p _build/gettext && ./doc_builder.sh", shell=True
    )
