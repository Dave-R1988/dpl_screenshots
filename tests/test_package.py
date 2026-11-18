from unittest.mock import Mock, call


def test_package_imports():
    import dpl_screenshots

    assert dpl_screenshots.__file__ is not None


def test_main_prints_ocr_result(monkeypatch, capsys):
    import dpl_screenshots.main as main_module

    getimagetext = Mock(side_effect=["recognized text 0", "recognized text 1"])
    get_lcs_length = Mock(return_value=12)
    monkeypatch.setattr(main_module, "getimagetext", getimagetext)
    monkeypatch.setattr(main_module, "get_lcs_length", get_lcs_length)

    main_module.main(["sample0.png", "sample1.png"])

    assert getimagetext.call_args_list == [
        call("sample0.png"),
        call("sample1.png"),
    ]
    get_lcs_length.assert_called_once_with(
        "recognized text 0",
        "recognized text 1",
    )
    assert capsys.readouterr().out == (
        "recognized text 0\n"
        "recognized text 1\n"
        "12\n"
    )
