# src/ui/views/package_detail.py
from gi.repository import Gtk
from src.controllers.package_manager import PackageManager

class PackageDetailView(Gtk.Box):
    def __init__(self, main_window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.main_window = main_window
        self.package_manager = PackageManager()
        
        # Labels for package details
        self.package_name_label = Gtk.Label(label="Package Name:")
        self.package_description_label = Gtk.Label(label="Description:")
        
        # Pack into layout
        self.pack_start(self.package_name_label, False, False, 0)
        self.pack_start(self.package_description_label, False, False, 0)

    def load_package(self, package_name):
        package_info = self.package_manager.get_package_info(package_name)
        if package_info:
            self.package_name_label.set_text(f"Package Name: {package_info['name']}")
            self.package_description_label.set_text(f"Description: {package_info['description']}")
            self.show_use_flags(package_info['name'])  # New method to show USE flags
    
    def show_use_flags(self, package_name):
        # Example method to display and manage USE flags
        use_flags = self.package_manager.get_use_flags(package_name)
        for flag in use_flags:
            checkbox = Gtk.CheckButton(label=flag['name'])
            checkbox.set_active(flag['enabled'])
            checkbox.connect("toggled", self.on_use_flag_toggled, flag['name'])
            self.pack_start(checkbox, False, False, 0)

    def on_use_flag_toggled(self, checkbox, flag_name):
        is_checked = checkbox.get_active()
        self.package_manager.toggle_use_flag(flag_name, is_checked)  # Control USE flags
