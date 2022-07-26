# PDM-VSCode

![Github Actions](https://github.com/frostming/pdm-vscode/workflows/Tests/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/pdm-vscode?logo=python&logoColor=%23cccccc)](https://pypi.org/project/pdm-vscode)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

A PDM plugin that autogenerates workspace vscode settings for you

## Installation

Install the plugin with PDM CLI:

```bash
pdm plugin add pdm-vscode
```

Or using `pipx inject`:

```bash
pipx inject pdm pdm-vscode
```

## Usage

No configuration is required, `.vscode/settings.json` will be autogenerated after `pdm init` and every execution of `pdm use`.
