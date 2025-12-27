"""Conftest."""

from __future__ import annotations

import os
import typing

import pytest

from pytest_checkers import (
    GROUP_NAME,
    HELPS,
    Group,
    Tool,
)

pytest_plugins = ["pytester"]


@pytest.fixture
def checkers_module(pytestconfig: pytest.Config) -> typing.Any:
    """Retrieve the actual module instance registered as a plugin."""
    return pytestconfig.pluginmanager.get_plugin("checkers")


@pytest.fixture(scope="session")
def tested_tools() -> list[str] | None:
    """Tested tools from tox environment variable."""
    tested_tools_ = os.environ.get("TESTED_TOOLS")
    if tested_tools_ is None:
        return None
    return tested_tools_.split(",")


def _tool_names() -> tuple[Tool]:
    return typing.get_args(Tool)


@pytest.fixture(params=_tool_names(), ids=lambda p: p)
def tool(request: pytest.FixtureRequest) -> typing.Any:
    """Tool name."""
    return request.param


@pytest.fixture
def helps() -> dict[Tool | Group, str]:
    """Help dictionary."""
    return HELPS.copy()


@pytest.fixture
def checkers_help() -> str:
    """Checkers help."""
    return HELPS[GROUP_NAME]


def _tool_help() -> list[tuple[Tool, str]]:
    return [(k, v) for k, v in HELPS.items() if k != GROUP_NAME]


@pytest.fixture(params=_tool_help(), ids=lambda p: p[0])
def tool_help(request: pytest.FixtureRequest) -> typing.Any:
    """Tool name and help."""
    return request.param


@pytest.fixture
def tool_flags() -> dict[Tool, list[str]]:
    """Tool flags."""
    return {
        "pyright": [],
        "ty": ["check"],
        "mypy": [],
        "ruff": ["check"],
        "flake8": ["--color=always"],
        "black": ["--diff", "--color"],
        "isort": ["--diff", "--color"],
    }


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Dynamically parameterize tests using the registered plugin's tools_map."""
    checkers = metafunc.config.pluginmanager.get_plugin("checkers")
    if checkers is None:
        return
    if "tool_map" in metafunc.fixturenames:
        metafunc.parametrize(
            "tool_map",
            checkers.tools_map.items(),
            ids=lambda p: p[0],
        )
    if "custom_is_error" in metafunc.fixturenames:
        metafunc.parametrize(
            "custom_is_error",
            [
                ("BlackPlugin", "some change\n@@ -1,1 +1,1 @@", True),
                ("BlackPlugin", "Success", False),
                ("IsortPlugin", "Fixing imports\n@@", True),
                ("IsortPlugin", "Nothing to do", False),
            ],
            ids=["black-error", "black-noerror", "isort-error", "isort-noerror"],
        )
