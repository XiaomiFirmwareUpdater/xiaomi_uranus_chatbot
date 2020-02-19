""" Xiaomi Geeks chat Bot localization class."""
from glob import glob

import yaml

from uranus_bot import WORK_DIR


class Localize:
    def __init__(self):
        self.locales = self.get_available_locales()
        self.text = self.load_text()

    @staticmethod
    def get_available_locales() -> list:
        return [lang.split('/')[-1].split('.')[0] for lang in glob(f"{WORK_DIR}/i18n/*.yml")
                if not lang.endswith("locales.yml")]

    def load_text(self) -> dict:
        text = {}
        for locale in self.locales:
            with open(f"{WORK_DIR}/i18n/{locale}.yml", "r") as yaml_file:
                text.update({locale: yaml.load(yaml_file, Loader=yaml.FullLoader)})
        return text

    def get_text(self, locale, text):
        return self.text[locale][text]
