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
        self.package_name_label.set_text(f"Package Name: {package_info['name']}")
        self.package_description_label.set_text(f"Description: {package_info['description']}")

