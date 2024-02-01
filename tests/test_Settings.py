from source.settings import Settings

def test_get_setting() -> None:
    settings_info = Settings("./tests/test_data/sample_settings_file.yaml")
    assert settings_info.get_setting("ask_when_exit") is True
    assert settings_info.get_setting("tem_dir") is None
