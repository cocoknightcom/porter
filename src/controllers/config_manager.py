# src/controllers/config_manager.py
from src.utils.file_utils import read_file, write_file

class ConfigManager:
    def __init__(self, config_path="/etc/portage/make.conf"):
        self.config_path = config_path

    def read_config(self):
        return read_file(self.config_path)

    def write_config(self, content):
        write_file(self.config_path, content)

