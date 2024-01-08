from typing import Any
import yaml


class Settings():
    def __init__(self, file_path:str) -> None:
        self.settings_file_path: str = file_path
        self._settings: dict = {}
        self._load_settings()

    def _load_settings(self) -> None:
        try:
            with open(self.settings_file_path, "r", encoding="utf-8") as file:
                self._settings = yaml.safe_load(file)
        except FileNotFoundError:
            self.create_settings_file()
 
    def create_settings_file(self) -> None:
        with open("./source/default_settings.yaml", "r", encoding="utf-8") as default_settings:
            content: str = default_settings.read()
            with open(self.settings_file_path, "w", encoding="utf-8") as file:
                file.write(content)

    def save_settings(self) -> None:
        with open(self.settings_file_path, "w", encoding="utf-8") as file:
            yaml.safe_dump(self._settings, file,
                           default_flow_style=False,
                           sort_keys=False)

    def get_setting(self, key, default=None) -> Any:
        return self._settings.get(key, default)

    def set_setting(self, key: str, value: Any) -> None:
        self._settings[key] = value
        self.save_settings()

if __name__ == "__main__":
    print("this is a module for import only")

# Author: Anh-Minh Do, 01.2024, Potsdam, Germany
# License: MIT
