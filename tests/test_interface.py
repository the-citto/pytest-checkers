"""Test behaviour."""

from __future__ import annotations

import typing

import pytest

from pytest_checkers import GROUP_NAME

if typing.TYPE_CHECKING:
    from pytest_checkers import (
        Group,
        Tool,
    )


class TestPytestHelp:
    """Test pytest help section."""

    _cached_result: pytest.RunResult | None = None

    @pytest.fixture
    def result(self, pytester: pytest.Pytester) -> pytest.RunResult:
        """Run pytest help."""
        if self._cached_result is None:
            self._cached_result = pytester.runpytest_subprocess("--help")
        return self._cached_result

    def test_group(self, result: pytest.RunResult) -> None:
        """Test pytest group."""
        result.stdout.fnmatch_lines([f"{GROUP_NAME}*"])

    def test_checkers_flag(self, result: pytest.RunResult, helps: dict[Tool | Group, str]) -> None:
        """Test checkers flag."""
        checkers_help = helps.get(GROUP_NAME)
        result.stdout.fnmatch_lines([f"*--{GROUP_NAME}*{checkers_help}"])

    def test_tool_flag(
        self,
        result: pytest.RunResult,
        tested_tools: list[str] | None,
        tool_help: tuple[str, str],
    ) -> None:
        """Test tool flag."""
        tool_, help_ = tool_help
        help_txt = f"*--{tool_}*{help_}"
        if tested_tools is None or tool_ in tested_tools:
            result.stdout.fnmatch_lines([help_txt])
        else:
            result.stdout.no_fnmatch_line(help_txt)


class TestSummaries:
    """Test summaries."""

    @pytest.fixture
    def dummy_test_file(self, pytester: pytest.Pytester) -> None:
        """Return dummy test file."""
        file_txt = '"""Test dummy."""\n\n\ndef test_dummy() -> None:\n    """Test dummy."""\n'
        file_path = pytester.path / "test_dummy.py"
        file_path.write_text(file_txt, encoding="utf-8")

    @pytest.fixture
    def valid_result(self, pytester: pytest.Pytester, dummy_test_file: None, tool: str) -> pytest.RunResult:
        """Get valid result."""
        _ = dummy_test_file
        file_path = pytester.path / "dummy_file.py"
        file_path.write_text('"""Test doc."""\n', encoding="utf-8")
        return pytester.runpytest_subprocess(f"--{tool}")

    @pytest.fixture
    def invalid_result(self, pytester: pytest.Pytester, dummy_test_file: None, tool: str) -> pytest.RunResult:
        """Get invalid result."""
        _ = dummy_test_file
        pytester.makepyfile("import os\n\n\nimport re\n\n\ndef dummy(dummy_arg) -> None:\n    return 'bar'")
        return pytester.runpytest_subprocess(f"--{tool}")

    def test_tool_header(self, tested_tools: list[str] | None, tool: str, valid_result: pytest.RunResult) -> None:
        """Test tool header."""
        header_txt = f"*=== tests {tool} ===*"
        if tested_tools is None or tool in tested_tools:
            valid_result.stdout.fnmatch_lines([header_txt])
        else:
            valid_result.stdout.no_fnmatch_line(header_txt)

    def test_valid_summary(self, tested_tools: list[str] | None, tool: str, valid_result: pytest.RunResult) -> None:
        """Test valid summary."""
        if tested_tools is None or tool in tested_tools:
            valid_result.assert_outcomes(passed=2, errors=0, failed=0)
        else:
            valid_result.stderr.fnmatch_lines(
                [
                    f"*error: unrecognized arguments: --{tool}*",
                ],
            )

    def test_invalid_summary(self, tested_tools: list[str] | None, tool: str, invalid_result: pytest.RunResult) -> None:
        """Test invalid summary."""
        if tested_tools is None or tool in tested_tools:
            invalid_result.assert_outcomes(passed=1, failed=1)
        else:
            invalid_result.stderr.fnmatch_lines(
                [
                    f"*error: unrecognized arguments: --{tool}*",
                ],
            )

    def test_valid_code(self, tested_tools: list[str] | None, tool: str, valid_result: pytest.RunResult) -> None:
        """Test valid code."""
        if tested_tools is None or tool in tested_tools:
            assert valid_result.ret == 0, "Expected 'All tests were collected and passed successfully'"
        else:
            assert valid_result.ret == 4, "Expected 'pytest command line usage error'"

    def test_invalid_code(self, tested_tools: list[str] | None, tool: str, invalid_result: pytest.RunResult) -> None:
        """Test invalid code."""
        if tested_tools is None or tool in tested_tools:
            assert invalid_result.ret == 1, "Expected 'Test execution was interrupted by the user'"
        else:
            assert invalid_result.ret == 4, "Expected 'pytest command line usage error'"
