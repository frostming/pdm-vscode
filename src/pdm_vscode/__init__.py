from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pdm.core import Core


def main(core: Core):
    from pdm.signals import post_init, post_use

    from pdm_vscode.hook import generate_vscode_settings

    post_init.connect(generate_vscode_settings)
    post_use.connect(generate_vscode_settings)
