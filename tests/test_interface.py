"""Test behaviour."""

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import pytest

    from tests.conftest import (
        ToolName,
    )

    # from tests.conftest import (
    #     ToolHelp,
    # )


# def test_pytest_help_option(pytester: pytest.Pytester, tool_help_data: ToolHelp) -> None:
#     """Test pytest help options."""
#     tool_name, help_ = tool_help_data
#     result = pytester.runpytest_subprocess("--help")
#     help_txt = f"*--{tool_name}*{help_}"
#     if TESTED_TOOL is None or TESTED_TOOL in ["checkers", tool_name]:
#         result.stdout.fnmatch_lines([help_txt])
#     else:
#         # assert help_txt not in result.stdout.str()
#         # result.stdout.no_fnmatch_line(help_txt)
#         assert TESTED_TOOL not in result.stdout.str()


def test_tool_header(pytester: pytest.Pytester, tested_tool: str | None, tool_name: ToolName) -> None:
    """Test tool header."""
    pytester.makepyfile('"""Test doc."""\n')
    result = pytester.runpytest_subprocess(f"--{tool_name}")
    header_txt = f"=== tests {tool_name} ==="
    if tested_tool is None or tested_tool == "checkers":
        return
    if tested_tool == tool_name:
        assert header_txt in result.stdout.str()
        # result.stdout.fnmatch_lines([header_txt])
    else:
        assert header_txt not in result.stdout.str()
        # result.stdout.no_fnmatch_line(header_txt)


# def test_tool_no_header(pytester: pytest.Pytester, tool_name: ToolName) -> None:
#     """Test tool no header."""
#     file_content = '"""Test doc."""\n'
#     file_path = pytester.path / "dummy_file.py"
#     file_path.write_text(file_content)
#     result = pytester.runpytest_subprocess(f"--{tool_name}")
#     assert f"===* tests {tool_name} ===*" not in result.stdout.str()
#
#
# def test_tool_footer(pytester: pytest.Pytester, tool_name: ToolName) -> None:
#     """Test tool footer."""
#     file_content = '"""Test doc."""\n'
#     file_path = pytester.path / "dummy_file.py"
#     file_path.write_text(file_content)
#     result = pytester.runpytest_subprocess(f"--{tool_name}")
#     result.stdout.fnmatch_lines(["===* 1 passed in *===*"])
#
#
# def test_tool_summary_passed(pytester: pytest.Pytester, tool_name: ToolName) -> None:
#     """Test summary code passed."""
#     file_content = '"""Test doc."""\n'
#     file_path = pytester.path / "dummy_file.py"
#     file_path.write_text(file_content)
#     result = pytester.runpytest_subprocess(f"--{tool_name}")
#     result.assert_outcomes(passed=1)
#
#
# def test_tool_summary_failed(pytester: pytest.Pytester, tool_name: ToolName) -> None:
#     """Test summary code failed."""
#     file_content = "import foo\n\n\nimport bar\n-\n\n"
#     file_path = pytester.path / "dummy_file.py"
#     file_path.write_text(file_content)
#     result = pytester.runpytest_subprocess(f"--{tool_name}")
#     result.assert_outcomes(failed=1)
