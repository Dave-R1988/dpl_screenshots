from unittest.mock import Mock

import pytest


def test_package_imports():
    import dpl_screenshots

    assert dpl_screenshots.__file__ is not None


@pytest.mark.parametrize(
    ("command", "handler_name"),
    [
        ("analyze-imagetexts", "analyze_imagetexts"),
        ("analyze-imagehistograms", "analyze_imagehistograms"),
    ],
)
def test_main_dispatches_to_handler(command, handler_name, monkeypatch):
    import dpl_screenshots.main as main_module

    handler = Mock()
    monkeypatch.setattr(main_module, handler_name, handler)
    main_module.main([command, "/nas/screenshots"])

    handler.assert_called_once_with("/nas/screenshots")


@pytest.mark.parametrize(
    "command",
    ["analyze-imagetexts", "analyze-imagehistograms"],
)
def test_analysis_subcommands_require_screenshots_path(command, capsys):
    import dpl_screenshots.main as main_module

    with pytest.raises(SystemExit) as error:
        main_module.main([command])

    assert error.value.code == 2
    assert "screenshots_path" in capsys.readouterr().err
