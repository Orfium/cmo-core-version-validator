import ntpath
import os
from enum import Enum

import toml
from github import Github
from packaging import version
from wheel_filename import parse_wheel_filename

from logging import getLogger

logger = getLogger(__name__)

GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
CURRENT_REPO = os.getenv("CURRENT_REPO")
CURRENT_HASH = os.getenv("CURRENT_HASH")
CURRENT_REQUIREMENTS_FILE = os.getenv("CURRENT_REQUIREMENTS_FILE")
CURRENT_REQUIREMENTS_FILE_FORMAT = os.getenv(
    "CURRENT_REQUIREMENTS_FILE_FORMAT")
REF_REPO = os.getenv("REF_REPO")
REF_HASH = os.getenv("REF_HASH")
REF_REQUIREMENTS_FILE = os.getenv("REF_REQUIREMENTS_FILE")
REF_REQUIREMENTS_FILE_FORMAT = os.getenv("REF_REQUIREMENTS_FILE_FORMAT")


class RequirementsType(Enum):
    POETRY_TOML = "toml"
    PIP_REQUIREMENTS = "txt"
    SETUP_TOOLS = "setup_tools"


def get_cmo_core_version_from_file(
        contents,
        file_type=RequirementsType.PIP_REQUIREMENTS.value
):
    mapping = {
        RequirementsType.PIP_REQUIREMENTS.value: __get_cmo_core_version_from_pip_requirements,
        RequirementsType.POETRY_TOML.value: __get_cmo_core_version_from_poetry_toml
    }
    return mapping[file_type](contents)


def __get_cmo_core_version_from_poetry_toml(contents):
    requirements_dict = toml.loads(contents.decode("utf-8"))
    try:
        core_str = \
            requirements_dict["tool"]["poetry"]["dependencies"]["cmo-core"][
                "url"]
    except KeyError:
        raise KeyError("cmo-core is not found in toml file")
    tail = ntpath.basename(core_str)
    return parse_wheel_filename(tail).version


def __get_cmo_core_version_from_pip_requirements(contents):
    requirements_lines = contents.decode("utf-8")
    lines = requirements_lines.split("\n")
    for line in lines:
        if "cmo-core" in line:
            tail = ntpath.basename(line)
            return parse_wheel_filename(tail).version
    raise KeyError("cmo-core not found in requirements file")


def main():
    gh_client = Github(
        GITHUB_ACCESS_TOKEN
    )

    gh_src = gh_client.get_repo(CURRENT_REPO).get_contents(
        CURRENT_REQUIREMENTS_FILE, ref=CURRENT_HASH)
    gh_dst = gh_client.get_repo(REF_REPO).get_contents(REF_REQUIREMENTS_FILE,
                                                       ref=REF_HASH)

    src_core_version = get_cmo_core_version_from_file(
        contents=gh_src.decoded_content,
        file_type=CURRENT_REQUIREMENTS_FILE_FORMAT
    )
    dst_core_version = get_cmo_core_version_from_file(
        contents=gh_dst.decoded_content,
        file_type=REF_REQUIREMENTS_FILE_FORMAT
    )

    if version.parse(src_core_version) < version.parse(dst_core_version):
        raise AssertionError(
            f"{src_core_version} is incompatible with {dst_core_version} "
        )


if __name__ == '__main__':
    main()
