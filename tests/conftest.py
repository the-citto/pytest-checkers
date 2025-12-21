"""Conftest."""

from __future__ import annotations

import os
import typing

import pytest

from pytest_checkers import checkers

pytest_plugins = ["pytester"]

# TESTED_TOOL = os.environ.get("TESTED_TOOL")
# SKIP_MSG = "'{tool_name}' skipped, tested tool is '{tested_tool}'"

ToolHelp = tuple[str, str]
ToolName = str

_tool_names: list[ToolName] = list(checkers.TOOLS_MAP)


@pytest.fixture(scope="session")
def tested_tool() -> str | None:
    """Tested tool from tox environment variable."""
    return os.environ.get("TESTED_TOOL")


def _tool_help_data() -> list[ToolHelp]:
    out = [("checkers", checkers.CHECKERS_HELP)]
    out.extend((k, v["help_"]) for k, v in checkers.TOOLS_MAP.items())
    return out


def _tool_help_ids(value: tuple[str, str]) -> str:
    tool_name, _ = value
    return f"tool_option:{tool_name}"


@pytest.fixture(params=_tool_help_data(), ids=_tool_help_ids, scope="session")
def tool_help_data(request: pytest.FixtureRequest) -> typing.Any:
    """Tool and help data."""
    return request.param


@pytest.fixture(params=_tool_names, ids=lambda v: f"tool_option:{v}", scope="session")
def tool_name(request: pytest.FixtureRequest) -> typing.Any:
    """Tool name."""
    return request.param


# def pytest_runtest_setup(item: pytest.Item) -> None:
#     """Set hook."""
#     tested_tool = os.environ.get("TESTED_TOOL")
#     if not isinstance(item, pytest.Function):
#         return
#     if "tool_name" not in item.fixturenames:
#         return
#     # tool_name = item.funcargs.get("tool_name")
#     tool_name = item.callspec.params.get("tool_name")
#     if tool_name is None:
#         return
#     is_tested_tool = tested_tool in ["checkers", tool_name]
#     skip_msg = SKIP_MSG.format(tool_name=tool_name, tested_tool=tested_tool)
#     if (item.get_closest_marker("tool_name_only") and not is_tested_tool) or (
#         item.get_closest_marker("tool_name_skipped") and is_tested_tool
#     ):
#         pytest.skip(skip_msg)
#     # if item.get_closest_marker("tool_name_skipped"):
#     #     return
#     # if tested_tool not in ["checkers", tool_name]:  # ty: ignore[unsupported-operator]
#     #     xfail_msg = XFAIL_MSG.format(tool_name=tool_name, tested_tool=tested_tool)
#     #     item.add_marker(pytest.mark.xfail(reason=xfail_msg, strict=True))
