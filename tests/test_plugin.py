import json
import os
import shutil
import sys
from pathlib import Path

import pytest
from pdm.core import Core
from pdm.project import Project

TEMPLATE_PYPROJECT = Path(__file__).parent / "pyproject.toml"


@pytest.fixture()
def tmp_project(tmp_path: Path) -> Project:
    shutil.copy2(TEMPLATE_PYPROJECT, tmp_path / "pyproject.toml")
    core = Core()
    return core.create_project(tmp_path)


def test_pdm_autoexport(tmp_project: Project):
    tmp_project.core.main(["init", "-n"], obj=tmp_project)
    settings = tmp_project.root / ".vscode" / "settings.json"
    assert settings.exists()
    extra_path = os.path.join(
        "${workspaceFolder}", "__pypackages__", tmp_project.python.identifier, "lib"
    )
    terminal_integrated_env_settings = {}
    if sys.platform.startswith("linux"):
        terminal_integrated_env_settings = {"terminal.integrated.env.linux": {"PYTHONPATH": extra_path}}
    elif sys.platform.startswith("darwin"):
        terminal_integrated_env_settings = {"terminal.integrated.env.osx": {"PYTHONPATH": extra_path}}
    elif sys.platform.startswith("win32"):
        terminal_integrated_env_settings = {"terminal.integrated.env.windows": {"PYTHONPATH": extra_path}}
    assert json.loads(settings.read_text()) == {
        "python.analysis.extraPaths": [extra_path],
        "python.autoComplete.extraPaths": [extra_path],
        **terminal_integrated_env_settings,
    }
    tmp_project.core.main(["venv", "create"], obj=tmp_project)
    if os.name == "nt":
        python = str(tmp_project.root / ".venv" / "Scripts" / "python.exe")
    else:
        python = str(tmp_project.root / ".venv" / "bin" / "python")
    tmp_project.core.main(["use", "-f", python], obj=tmp_project)
    # TODO: a bug to be fixed in PDM
    # assert json.loads(settings.read_text()) == {}
