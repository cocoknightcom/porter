from gi.repository import Gtk
from src.controllers.config_manager import ConfigManager

class SettingsView(Gtk.Box):
    def __init__(self, main_window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.main_window = main_window
        self.config_manager = ConfigManager()
        
        # Title Label for settings
        title_label = Gtk.Label(label="Settings")
        self.pack_start(title_label, False, False, 0)

        # Additional settings widgets can be added here

