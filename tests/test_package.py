def test_package_imports():
    import dpl_screenshots

    assert dpl_screenshots.__file__ is not None


def test_main_prints_help_without_arguments(capsys):
    from dpl_screenshots.main import main

    main([])

    assert "usage: dpl-screenshots" in capsys.readouterr().out
