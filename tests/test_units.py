"""Test unit."""

from __future__ import annotations

import pathlib
import sys
import typing
from unittest.mock import (
    MagicMock,
    patch,
)

import pytest

if typing.TYPE_CHECKING:
    import types

    from pytest_checkers import Tool
    from pytest_checkers.checkers import CheckersPlugin


class TestPluginItem:
    """TestPluginItem."""

    @pytest.fixture
    def mock_plugin(self, checkers_module: types.ModuleType) -> MagicMock:
        """Mock plugin."""
        plugin = MagicMock(spec=checkers_module.CheckersPlugin)
        plugin.is_error = False
        plugin.cmd_output = ""
        return plugin

    @pytest.fixture
    def item_setup(
        self,
        checkers_module: types.ModuleType,
        mock_plugin: MagicMock,
    ) -> tuple[pytest.Item, MagicMock]:
        """Initialize PluginItem with mocked pytest internals."""
        mock_config = MagicMock()
        mock_config.pluginmanager.get_plugin.return_value = mock_plugin
        item = checkers_module.PluginItem.from_parent(
            parent=MagicMock(),
            name="test_plugin",
            path=pathlib.Path("dummy_path"),
        )
        item.config = mock_config  # ty: ignore[invalid-assignment]
        return item, mock_plugin

    def test_runtest_success(self, item_setup: tuple[pytest.Item, MagicMock]) -> None:
        """Test `runtest` success."""
        item_obj, mock_plugin = item_setup
        item_obj.runtest()
        mock_plugin.run_tool.assert_called_once()

    def test_runtest_failure(self, item_setup: tuple[pytest.Item, MagicMock]) -> None:
        """Test `runtest` failure."""
        item_obj, mock_plugin = item_setup
        mock_plugin.is_error = True
        mock_plugin.cmd_output = "Error: something went wrong"
        with pytest.raises(pytest.fail.Exception, match="failed with output"):
            item_obj.runtest()

    def test_repr_failure(self, item_setup: tuple[pytest.Item, MagicMock]) -> None:
        """Test `repr_failure`."""
        item_obj, _ = item_setup
        res = item_obj.repr_failure(MagicMock())  # ty: ignore[invalid-argument-type]
        assert res == "test_plugin failed with output..."

    def test_reportinfo(self, item_setup: tuple[pytest.Item, MagicMock]) -> None:
        """Test `reportinfo`."""
        item_obj, _ = item_setup
        path, line, msg = item_obj.reportinfo()
        assert path == pathlib.Path("dummy_path")
        assert line == 0
        assert msg == "tool::test_plugin"


class TestCheckersPlugin:
    """TestCheckersPlugin."""

    @pytest.fixture
    def dummy_tool(self) -> str:
        """Set dummy tool."""
        return "dummy_tool"

    @pytest.fixture
    def dummy_class(self, checkers_module: types.ModuleType, dummy_tool: str) -> CheckersPlugin:
        """Return dummy abstract class."""

        class _DummyPlugin(checkers_module.CheckersPlugin):  # type: ignore[name-defined,misc]

            tool = dummy_tool

        mock_config = MagicMock(spec=pytest.Config)
        return _DummyPlugin(config=mock_config)

    def test_init(self, dummy_class: CheckersPlugin) -> None:
        """Test `__init__`."""
        assert hasattr(dummy_class, "config")
        assert isinstance(dummy_class.config, pytest.Config)
        assert dummy_class.cmd_output == ""
        assert dummy_class.cmd_returncode == 0

    def test_env_vars(self, dummy_class: CheckersPlugin) -> None:
        """Test `env_vars`."""
        assert dummy_class.env_vars.get("FORCE_COLOR") == "1"
        assert dummy_class.env_vars.get("MYPY_FORCE_COLOR") == "1"

    def test_is_error_false(self, dummy_class: CheckersPlugin) -> None:
        """Test `is_error` false."""
        assert not dummy_class.is_error

    def test_is_error_true(self, dummy_class: CheckersPlugin) -> None:
        """Test `is_error` true."""
        dummy_class.cmd_returncode = 1
        assert dummy_class.is_error

    def test_run_tool(self, dummy_class: CheckersPlugin, dummy_tool: str) -> None:
        """Test `run_tool`."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value(returncode=0)
            dummy_class.run_tool()
            expected_cmd = [sys.executable, "-m", dummy_tool, str(dummy_class.config.rootpath)]
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            assert args[0] == expected_cmd
            assert kwargs["env"] == dummy_class.env_vars

    def test_pytest_terminal_summary(self, dummy_class: CheckersPlugin) -> None:
        """Test `pytest_terminal_summary`."""
        dummy_class.header_markup = "green"
        dummy_class.cmd_output = "Success"
        dummy_class.finish_msg = " Done."
        mock_reporter = MagicMock()
        dummy_class.pytest_terminal_summary(mock_reporter)  # ty: ignore[invalid-argument-type]
        mock_reporter.write_sep.assert_called_once_with(
            title=f"tests {dummy_class.tool}",
            sep="=",
            green=True,
        )
        mock_reporter.write.assert_called_once_with("Success Done.")

    def test_pytest_collection_modifyitems(self, dummy_class: CheckersPlugin) -> None:
        """Test `pytest_collection_modifyitems`."""
        mock_session = MagicMock(spec=pytest.Session)
        mock_config = MagicMock(spec=pytest.Config)
        items: list[pytest.Item] = []
        with patch("pytest_checkers.checkers.PluginItem") as mock_plugin_item_class:
            mock_created_item = MagicMock()
            mock_plugin_item_class.from_parent.return_value = mock_created_item
            dummy_class.pytest_collection_modifyitems(
                session=mock_session,  # ty: ignore[invalid-argument-type]
                config=mock_config,  # ty: ignore[invalid-argument-type]
                items=items,
            )
            mock_plugin_item_class.from_parent.assert_called_once_with(
                mock_session,
                name=dummy_class.tool,
            )
            assert mock_created_item._nodeid.endswith(  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
                f"::{dummy_class.tool}",
            )
            assert len(items) == 1
            assert items[0] == mock_created_item


class TestToolPlugin:
    """TestPyrightPlugin."""

    @pytest.fixture
    def tool_instance(self, tool_map: tuple[Tool, type[CheckersPlugin]]) -> CheckersPlugin:
        """Return tool instance."""
        _, tool_class = tool_map
        mock_config = MagicMock(spec=pytest.Config)
        return tool_class(config=mock_config)  # ty: ignore[invalid-argument-type]

    def test_tool_attrs(self, tool_instance: CheckersPlugin, tool_map: tuple[Tool, type[CheckersPlugin]]) -> None:
        """Test tool attributes."""
        tool_name, _ = tool_map
        assert tool_instance.tool == tool_name
        assert isinstance(tool_instance.header_markup, str)

    def test_cmd_flag(
        self,
        tool_instance: CheckersPlugin,
        tool_map: tuple[Tool, type[CheckersPlugin]],
        tool_flags: dict[Tool, list[str]],
    ) -> None:
        """Test `cmd_flag`."""
        tool_name, _ = tool_map
        assert tool_instance.cmd_flags == tool_flags[tool_name]

    def test_is_error_custom(self, checkers_module: types.ModuleType, custom_is_error: tuple[str, str, bool]) -> None:
        """Test custom `is_error`."""
        tool_class_name, cmd_output, expected = custom_is_error
        tool_class = getattr(checkers_module, tool_class_name)
        plugin = tool_class(config=MagicMock())
        plugin.cmd_output = cmd_output
        assert plugin.is_error is expected


def test_pytest_configure_checkers(
    checkers_module: CheckersPlugin,
    tool_map: tuple[Tool, type[CheckersPlugin]],
) -> None:
    """Test `pytest_configure` checkers selection."""
    tool_name, tool_class = tool_map
    mock_config = MagicMock()
    setattr(mock_config.option, tool_name, False)
    mock_config.option.checkers = True
    with patch("pytest_checkers.checkers.added_options", [tool_name]):
        checkers_module.pytest_configure(mock_config)  # type: ignore[attr-defined]
        mock_config.pluginmanager.register.assert_called_once()
        args, _ = mock_config.pluginmanager.register.call_args
        assert isinstance(args[0], tool_class)


def test_pytest_configure_tool(checkers_module: CheckersPlugin, tool_map: tuple[Tool, type[CheckersPlugin]]) -> None:
    """Test `pytest_configure` tool selection."""
    tool_name, tool_class = tool_map
    mock_config = MagicMock()
    mock_config.option.checkers = False
    setattr(mock_config.option, tool_name, True)
    with patch("pytest_checkers.checkers.added_options", [tool_name]):
        checkers_module.pytest_configure(mock_config)  # type: ignore[attr-defined]
        mock_config.pluginmanager.register.assert_called_once()
        args, _ = mock_config.pluginmanager.register.call_args
        assert isinstance(args[0], tool_class)
