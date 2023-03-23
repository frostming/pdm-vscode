from __future__ import annotations

import contextlib
import json
import os
import sys
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

    from pdm.models.python import PythonInfo
    from pdm.project import Project


class VSCodeSettings:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._data = self._read_settings()

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def delete(self, key: str) -> None:
        self._data.pop(key, None)

    def __enter__(self) -> VSCodeSettings:
        return self

    def __exit__(self, *args: Any) -> None:
        self._write_settings()

    def _read_settings(self) -> dict:
        with contextlib.suppress(OSError):
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _write_settings(self) -> None:
        with contextlib.suppress(OSError):
            if not self.path.parent.exists():
                self.path.parent.mkdir(parents=True)
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2)


def generate_vscode_settings(
    project: Project, python: PythonInfo | None = None, **kwargs: Any
) -> None:
    env = project.get_environment()
    with VSCodeSettings(project.root / ".vscode" / "settings.json") as settings:
        if env.is_global:
            settings.delete("python.analysis.extraPaths")
            settings.delete("python.autoComplete.extraPaths")
            settings.delete("terminal.integrated.env.linux")
            settings.delete("terminal.integrated.env.osx")
            settings.delete("terminal.integrated.env.windows")
            return
        if python is None:
            python = env.interpreter
        ident = python.identifier
        extra_path = os.path.join("${workspaceFolder}", "__pypackages__", ident, "lib")
        settings.set("python.analysis.extraPaths", [extra_path])
        settings.set("python.autoComplete.extraPaths", [extra_path])
        python_path = {"PYTHONPATH": extra_path}
        if sys.platform.startswith("linux"):
            settings.set("terminal.integrated.env.linux", python_path)
        elif sys.platform.startswith("darwin"):
            settings.set("terminal.integrated.env.osx", python_path)
        elif sys.platform.startswith("win32"):
            settings.set("terminal.integrated.env.windows", python_path)
