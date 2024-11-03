# src/ui/views/home_view.py
from gi.repository import Gtk
from src.controllers.package_manager import PackageManager
import os  # Import os to handle file icons

class HomeView(Gtk.Box):
    def __init__(self, parent):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.parent = parent
        self.package_manager = PackageManager()

        self.search_bar = Gtk.Entry()
        self.search_bar.set_placeholder_text("Search Packages")
        self.search_bar.set_property("width_chars", 30)
        self.search_bar.connect("activate", self.on_search_activated)
        self.pack_start(self.search_bar, False, False, 0)

        # Quick Actions row
        quick_actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.pack_start(quick_actions_box, False, False, 0)

        actions = [
            ("Update All", self.on_update_all_clicked),
            ("Sync Portage", self.on_sync_portage_clicked),
            ("Installed Packages", self.on_view_installed_clicked),
            ("Categories", self.on_view_categories_clicked),
        ]
        for label, callback in actions:
            button = Gtk.Button(label=label)
            button.connect("clicked", callback)
            quick_actions_box.pack_start(button, True, True, 0)

        # User Installed Packages List
        self.packages_list = Gtk.ListBox()
        self.pack_start(self.packages_list, True, True, 0)
        self.load_installed_packages()

        # Notifications/Alerts section
        alerts_label = Gtk.Label(label="Notifications / Alerts")
        alerts_label.set_xalign(0)
        self.pack_start(alerts_label, False, False, 0)

        self.alerts_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.pack_start(self.alerts_box, False, False, 0)
        self.load_alerts()

    def load_installed_packages(self):
        world_packages = self.package_manager.get_world_packages()
        for package in world_packages:
            package_info = self.package_manager.get_package_info(package)
            row = self.create_package_row(package_info)
            self.packages_list.add(row)
        self.packages_list.show_all()

    def create_package_row(self, package_info):
        # Create a horizontal box for each package with an icon and description
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        # Use a placeholder icon. You may replace this with actual package icons.
        icon_path = "/path/to/icons/package.png"  # Replace with an actual icon path, if needed
        image = Gtk.Image.new_from_file(icon_path)
        box.pack_start(image, False, False, 0)

        # Package name and description
        name_label = Gtk.Label(label=package_info['name'], xalign=0)
        description_label = Gtk.Label(label=package_info['description'], xalign=0)
        
        box.pack_start(name_label, True, True, 0)
        box.pack_start(description_label, True, True, 0)
        
        return box

    def load_alerts(self):
        alerts = ["Update available for package X", "Portage sync needed"]
        for alert in alerts:
            label = Gtk.Label(label=alert)
            label.set_xalign(0)
            self.alerts_box.pack_start(label, False, False, 0)
        self.alerts_box.show_all()

    # Callback functions for quick actions
    def on_update_all_clicked(self, widget):
        print("Update All clicked")

    def on_sync_portage_clicked(self, widget):
        print("Sync Portage clicked")

    def on_view_installed_clicked(self, widget):
        print("View Installed Packages clicked")

    def on_view_categories_clicked(self, widget):
        print("View Categories clicked")
    
    def on_search_activated(self, entry):
        search_query = self.search_bar.get_text()
        matched_packages = self.package_manager.search_packages(search_query)
        self.update_suggested_packages(matched_packages)

    def update_suggested_packages(self, packages):
        # This part can be updated to refresh the packages list dynamically if required
        pass