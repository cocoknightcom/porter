# src/ui/views/home_view.py
from gi.repository import Gtk
from src.controllers.package_manager import PackageManager

class HomeView(Gtk.Box):
    def __init__(self, parent):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.parent = parent
        self.package_manager = PackageManager()

        # Search Bar
        self.search_bar = Gtk.Entry()
        self.search_bar.set_placeholder_text("Search Packages")
        self.search_bar.set_property("width_chars", 30)
        self.search_bar.connect("activate", self.on_search_activated)
        self.pack_start(self.search_bar, False, False, 0)

        # Quick Actions
        quick_actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.pack_start(quick_actions_box, False, False, 0)

        # Add quick action buttons for package management
        actions = [
            ("Update All", self.on_update_all_clicked),
            ("Sync Portage", self.on_sync_portage_clicked),
            ("View Installed Packages", self.on_view_installed_clicked),
            ("Categories", self.on_view_categories_clicked),
        ]

        for label, callback in actions:
            button = Gtk.Button(label=label)
            button.connect("clicked", callback)
            quick_actions_box.pack_start(button, True, True, 0)

        # User Installed Packages section
        self.pack_list_label = Gtk.Label(label="User Installed Packages")
        self.pack_list_label.set_xalign(0)
        self.pack_start(self.pack_list_label, False, False, 0)

        # Scrolled area for packages
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.pack_start(self.scrolled_window, True, True, 0)

        self.pack_list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.scrolled_window.add(self.pack_list_box)
        self.load_user_installed_packages()

        # Notifications/Alerts
        alerts_label = Gtk.Label(label="Notifications / Alerts")
        alerts_label.set_xalign(0)
        self.pack_start(alerts_label, False, False, 0)

        self.alerts_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.pack_start(self.alerts_box, False, False, 0)
        self.load_alerts()

    def load_user_installed_packages(self):
        user_installed_packages = self.package_manager.get_user_installed_packages()

        for package in user_installed_packages:
            package_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            
            # You can set a default icon or use package-specific icons if available
            icon_path = self.get_package_icon_path(package['name'])
            package_icon = Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file(icon_path))
            package_box.pack_start(package_icon, False, False, 0)

            package_name_label = Gtk.Label(label=package['name'])
            package_description_label = Gtk.Label(label=package['description'])
            
            package_box.pack_start(package_name_label, True, True, 0)
            package_box.pack_start(package_description_label, True, True, 0)

            self.pack_list_box.pack_start(package_box, False, False, 0)

        self.pack_list_box.show_all()

    def load_alerts(self):
        # Placeholder for alerts
        alerts = ["Update available for package X", "Portage sync needed"]
        for alert in alerts:
            label = Gtk.Label(label=alert)
            label.set_xalign(0)
            self.alerts_box.pack_start(label, False, False, 0)
        self.alerts_box.show_all()

    def get_package_icon_path(self, package_name):
        # Placeholder for icon retrieval logic
        # Return a default icon path until package-specific icons are created
        return "/path/to/default/icon.png"

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
        # Placeholder for matched package display logic
        pass