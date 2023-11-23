import pathlib

from setuptools import setup

import versioneer

description = "A Python wrapper for the Misskey API"
readme_file = pathlib.Path(__file__).parent / "README.md"
with readme_file.open(encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

extras_require = {
    "dev": ["isort", "mypy", "pre-commit", "ruff"],
    "ci": ["mypy", "ruff"],
    "speed": ["orjson"],
    "doc": ["sphinx", "furo", "sphinxcontrib_trio", "sphinx-intl", "numpydoc"],
}

packages = [
    "mipac",
    "mipac.abstract",
    "mipac.actions",
    "mipac.actions.admins",
    "mipac.errors",
    "mipac.manager",
    "mipac.manager.admins",
    "mipac.models",
    "mipac.types",
    "mipac.models.lite",
    "mipac.utils",
]

setup(
    name="mipac",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    install_requires=requirements,
    url="https://github.com/yupix/mipac",
    author="yupix",
    author_email="yupi0982@outlook.jp",
    license="MIT",
    python_requires=">=3.11, <4.0",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=packages,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.11",
        "Natural Language :: Japanese",
        "License :: OSI Approved :: MIT License",
    ],
    extras_require=extras_require,
)
