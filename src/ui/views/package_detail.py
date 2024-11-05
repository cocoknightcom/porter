# src/ui/views/package_detail.py
from gi.repository import Gtk
from src.controllers.package_manager import PackageManager

class PackageDetailView(Gtk.Box):
    def __init__(self, main_window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.main_window = main_window
        self.package_manager = PackageManager()

        # Create a loading spinner
        self.loading_spinner = Gtk.Spinner()
        self.loading_spinner.set_margin_top(20)
        self.pack_start(self.loading_spinner, False, False, 0)
        
        # Labels for package details
        self.package_name_label = Gtk.Label(label="Package Name:")
        self.package_description_label = Gtk.Label(label="Description:")
        
        # Pack into layout
        self.pack_start(self.package_name_label, False, False, 0)
        self.pack_start(self.package_description_label, False, False, 0)

    def load_package(self, package_name):
        self.loading_spinner.start()  # Start loading spinner
        GLib.idle_add(self._load_package_background, package_name)

    def _load_package_background(self, package_name):
        package_info = self.package_manager.get_package_info(package_name)
        if package_info:
            self.package_name_label.set_text(f"Package Name: {package_info['name']}")
            self.package_description_label.set_text(f"Description: {package_info['description']}")
            self.show_use_flags(package_name)
        self.loading_spinner.stop()  # Stop loading spinner
        return False  # Exit the idle function to not call it again
    
    def show_use_flags(self, package_name):
        # Clear previous flags
        self.foreach(lambda widget: self.remove(widget))

        use_flags = self.package_manager.get_use_flags(package_name)
        for flag in use_flags:
            checkbox = Gtk.CheckButton(label=flag)
            checkbox.set_active(flag in self.package_manager.get_use_flags(package_name))  # Determines if USE flag is currently set
            checkbox.connect("toggled", self.on_use_flag_toggled, flag)
            self.pack_start(checkbox, False, False, 0)

    def on_use_flag_toggled(self, checkbox, flag_name):
        is_checked = checkbox.get_active()
        self.package_manager.toggle_use_flag(flag_name, is_checked)  # Control USE flags
