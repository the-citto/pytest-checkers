"""Test unit."""

# from __future__ import annotations
#
# import typing
#
# import pytest
#
# if typing.TYPE_CHECKING:
#
#     from tests.conftest import (
#         ToolName,
#     )
#
#
# @pytest.mark.tool_name_only
# def test_tool_code_passed(pytester: pytest.Pytester, tool_name: ToolName) -> None:
#     """Test tool code passed."""
#     file_content = '"""Test doc."""\n'
#     file_path = pytester.path / "dummy_file.py"
#     file_path.write_text(file_content)
#     result = pytester.runpytest_subprocess(f"--{tool_name}")
#     assert result.ret == pytest.ExitCode.OK
#
#
# @pytest.mark.tool_name_only
# def test_tool_code_failed(pytester: pytest.Pytester, tool_name: ToolName) -> None:
#     """Test tool code failed."""
#     file_content = "import foo\n\n\nimport bar\n-\n\n"
#     file_path = pytester.path / "dummy_file.py"
#     file_path.write_text(file_content)
#     result = pytester.runpytest_subprocess(f"--{tool_name}")
#     assert result.ret == pytest.ExitCode.TESTS_FAILED
#
#
# class TestPluginItem:
#     """TestPluginItem."""
#
#
# class TestCheckersPlugin:
#     """TestCheckersPlugin."""
#
#     # def test_env_vars(self, tool_name: ToolName) -> None:
#     #     """Test env_vars."""
#     #     plugin = checkers.CheckersPlugin(tool_name)
#
#     # def env_vars(self) -> dict[str, str]:
#     #     """Environment variables."""
#     #     env_vars = os.environ.copy()
#     #     env_vars["FORCE_COLOR"] = "1"
#     #     env_vars["MYPY_FORCE_COLOR"] = "1"
#     #     return env_vars
#     #
#     # @property
#     # def is_error(self) -> bool:
#     #     """Tool-specific error logic."""
#     #     return self.cmd_returncode != 0
#     #
#     # def run_tool(self) -> None:
#     #     """Run tool."""
#     #     project_root = self.config.rootpath
#     #     cmd = [sys.executable, "-m", self.tool, *self.cmd_flags, str(project_root)]
#     #     result = subprocess.run(cmd, capture_output=True, text=True, check=False, env=self.env_vars)  # oqa: S603
#     #     self.cmd_output = result.stdout + result.stderr
#     #     self.cmd_returncode = result.returncode
#     #
#     # def pytest_terminal_summary(self, terminalreporter: TerminalReporter) -> None:
#     #     """Pytest terminal summary."""
#     #     if not getattr(self.config.option, self.tool, False):
#     #         return
#     #     # circumventing mypy quirk - https://github.com/python/mypy/issues/10023
#     #     header_markup_kwarg = {typing.cast("str", self.header_markup): True}
#     #     terminalreporter.write_sep(title=f"tests {self.tool}", sep="=", **header_markup_kwarg)
#     #     terminalreporter.write(self.cmd_output)
#     #
#     # def pytest_collection_modifyitems(
#     #     self,
#     #     session: pytest.Session,
#     #     config: pytest.Config,
#     #     items: list[pytest.Item],
#     # ) -> None:
#     #     """Pytest collection modify item."""
#     #     _ = config
#     #     item = PluginItem.from_parent(session, name=self.tool)  # pyright: ignore[reportUnknownMemberType]
#     #     items.append(item)


# import importlib.metadata
# import typing
# from unittest.mock import (
#     MagicMock,
#     patch,
# )
#
# import pytest
#
# from pytest_checkers import checkers
#
# if typing.TYPE_CHECKING:
#     import pytest_mock

# def test_env_vars
# def test_plugin_discovery(pytester: pytest.Pytester) -> None:
#     """Verify that the plugin adds its options to pytest help."""
#     result = pytester.runpytest("--help")
#     result.stdout.fnmatch_lines(
#         [
#             "*--checkers*Enable all available checks*",
#             "*--pyright*Enable pyright*",
#         ],
#     )
#
#
# def test_tool_pass(pytester: pytest.Pytester) -> None:
#     """Test that the plugin passes when the tool finds no issues."""
#     # Create a dummy file that passes (e.g., for pyright)
#     pytester.makepyfile(
#         """
#         def hello() -> str:
#             return "world"
#     """,
#     )
#
#     # Run pytest with the plugin flag
#     # Assuming your plugin is installed or in the PYTHONPATH
#     result = pytester.runpytest_subprocess("--pyright")
#
#     # Use 2025 standard assertions
#     result.assert_outcomes(passed=1)
#     assert result.ret == 0
#
#
# def test_tool_fail(pytester: pytest.Pytester) -> None:
#     """Test that the plugin fails when the tool (e.g., pyright) finds an error."""
#     # Create a dummy file with a type error
#     pytester.makepyfile(
#         """
#         def hello() -> str:
#             return 123  # Type error
#     """,
#     )
#
#     result = pytester.runpytest_subprocess("--pyright")
#
#     # Verify the failure is captured by your PluginItem
#     result.assert_outcomes(failed=1)
#     result.stdout.fnmatch_lines(
#         [
#             "*pyright failed with output:*",
#         ],
#     )
#     assert result.ret == 1
#
#
# def test_terminal_summary(pytester: pytest.Pytester) -> None:
#     """Verify the custom summary header appears in terminal output."""
#     pytester.makepyfile("def test_dummy(): pass")
#
#     result = pytester.runpytest_subprocess("--pyright")
#
#     # Check for your custom header defined in pytest_terminal_summary
#     result.stdout.fnmatch_lines(
#         [
#             "===* tests pyright ===*",
#         ],
#     )
#
#
# def test_plugin_item_runtest_fail(pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch) -> None:
#     """Unit test the runtest method by mocking the tool plugin."""
#
#     class MockPlugin:
#         tool = "pyright"
#         is_error = True
#         cmd_output = "Mock Error Output"
#
#         def run_tool(self) -> None:
#             pass
#
#     # Create the item
#     item = checkers.PluginItem.from_parent(pytester.getnode(pytester.makepyfile("")), name="pyright")
#     # Mock the plugin manager to return our mock plugin
#     monkeypatch.setattr(item.config.pluginmanager, "get_plugin", lambda name: MockPlugin())
#
#     with pytest.raises(pytest.fail.Exception, match="pyright failed with output:"):
#         item.runtest()
#
#
# def test_pytest_addoption(mocker: pytest_mock.MockerFixture) -> None:
#     """Test that options are added only for installed packages."""
#     mocker.patch.object(checkers, "added_options", [])
#     with patch("importlib.metadata.version") as mock_version:
#
#         def side_effect(tool_name: str) -> str:
#             if tool_name == "flake8":
#                 return "1.0.0"
#             # Simulate 'ruff' also being installed
#             if tool_name == "ruff":
#                 return "1.0.0"
#             raise importlib.metadata.PackageNotFoundError
#
#         mock_version.side_effect = side_effect
#         # Mock the Parser object. We rely on the mock to capture calls to getgroup/addoption
#         mock_parser = MagicMock(spec=pytest.Parser)
#         mock_group = MagicMock()
#         mock_parser.getgroup.return_value = mock_group
#         # Call the function under test
#         checkers.pytest_addoption(mock_parser)  # ty: ignore[invalid-argument-type]
#         # --- FIX: Assert on exact string values, not typing.Any ---
#         # The function calls addoption with static strings/actions defined in the code
#         expected_flake8_call = mocker.call("--flake8", action="store_true", help="Enable `flake8`")
#         expected_ruff_call = mocker.call("--ruff", action="store_true", help="Enable `ruff check`")
#         mock_group.addoption.assert_has_calls([expected_flake8_call, expected_ruff_call], any_order=True)
#         # Check that 'flake8' and 'ruff' were added to the added_options list
#         assert "flake8" in checkers.added_options
#         assert "ruff" in checkers.added_options
#         # Ensure tools that threw PackageNotFoundError are not in the list
#         assert "black" not in checkers.added_options
#
#
# def test_pytest_configure_checkers_all(mocker: pytest_mock.MockerFixture) -> None:
#     """Test that --checkers enables all available options."""
#     mock_config = mocker.Mock()
#     # We must ensure the nested 'pluginmanager.register' path works
#     mock_register = mock_config.pluginmanager.register
#     mock_config.option = mocker.Mock()
#     # Simulate that the user provided --checkers=True on the CLI
#     mock_config.option.checkers = True
#     # Simulate that 'flake8' and 'isort' were the added_options
#     mocker.patch.object(checkers, "added_options", ["flake8", "isort"])
#     # Call the function under test
#     checkers.pytest_configure(mock_config)
#     # Verify that both plugins were activated because --checkers was set
#     assert mock_config.option.flake8 is True
#     assert mock_config.option.isort is True
#     # Verify registration happened
#     assert mock_register.call_count == 2
#     mock_register.assert_any_call(mocker.ANY, name="flake8")
#     mock_register.assert_any_call(mocker.ANY, name="isort")
#
#
# def test_checkers_plugin_properties() -> None:
#     """Test abstract base class properties."""
#     # Create a mock config object
#     mock_config = MagicMock(spec=pytest.Config)
#
#     # Create a concrete mock class inheriting from CheckersPlugin to test abstract methods
#     class MockCheckPlugin(checkers.CheckersPlugin):
#         tool: checkers.Tool = "black"
#         header_markup: checkers.EscTable = "cyan"
#
#         @property
#         def cmd_flags(self) -> list[str]:
#             return ["--mock-flag"]
#
#     plugin_instance = MockCheckPlugin(mock_config)  # ty: ignore[invalid-argument-type]
#     # Test cmd_flags abstract property implementation
#     assert plugin_instance.cmd_flags == ["--mock-flag"]
#     # Test default is_error implementation (based on returncode)
#     plugin_instance.cmd_returncode = 0
#     assert plugin_instance.is_error is False
#     plugin_instance.cmd_returncode = 1
#     assert plugin_instance.is_error is True
#     # Test env_vars property
#     env = plugin_instance.env_vars
#     assert "FORCE_COLOR" in env
#     assert env["FORCE_COLOR"] == "1"
#     assert "MYPY_FORCE_COLOR" in env
#     assert env["MYPY_FORCE_COLOR"] == "1"
#
#
# def test_black_plugin_is_error_logic() -> None:
#     """Test Black specific error logic based on output content."""
#     mock_config = MagicMock(spec=pytest.Config)
#     plugin = checkers.BlackPlugin(mock_config)  # ty: ignore[invalid-argument-type]
#     plugin.cmd_output = ""
#     plugin.cmd_returncode = 0  # Default logic would say no error
#     assert plugin.is_error is False  # Black logic overrides to check output
#     plugin.cmd_output = "@@ code change @@"
#     assert plugin.is_error is True
#     plugin.cmd_output = "black fail to reformat a file"
#     assert plugin.is_error is True
#
#
# def test_isort_plugin_is_error_logic() -> None:
#     """Test Isort specific error logic based on output content."""
#     mock_config = MagicMock(spec=pytest.Config)
#     plugin = checkers.IsortPlugin(mock_config)  # ty: ignore[invalid-argument-type]
#     plugin.cmd_output = ""
#     assert plugin.is_error is False
#     plugin.cmd_output = "@@ import change @@"
#     assert plugin.is_error is True


# ODO(the-citto): #000 clean
