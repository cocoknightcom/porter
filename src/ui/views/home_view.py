# src/ui/views/home_view.py
from gi.repository import Gtk
from src.controllers.package_manager import PackageManager

class HomeView(Gtk.Box):
    def __init__(self, parent):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.parent = parent
        self.package_manager = PackageManager()

        # Create a search bar with a rounded entry and connect the signal
        self.search_bar = Gtk.Entry()
        self.search_bar.set_placeholder_text("Search Packages")
        self.search_bar.set_property("width_chars", 30)
        self.search_bar.connect("activate", self.on_search_activated)  # Connect signal for enter key
        self.pack_start(self.search_bar, False, False, 0)

        # Quick Actions row
        quick_actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.pack_start(quick_actions_box, False, False, 0)

        # Add quick action buttons
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

        # Suggested Packages section
        suggested_label = Gtk.Label(label="Suggested Packages")
        suggested_label.set_xalign(0)  # Align label to the left
        self.pack_start(suggested_label, False, False, 0)

        # Scrollable area for suggested packages
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.pack_start(self.scrolled_window, True, True, 0)

        self.suggested_packages_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.scrolled_window.add(self.suggested_packages_box)
        self.load_suggested_packages()

        # Notifications/Alerts section
        alerts_label = Gtk.Label(label="Notifications / Alerts")
        alerts_label.set_xalign(0)
        self.pack_start(alerts_label, False, False, 0)

        self.alerts_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.pack_start(self.alerts_box, False, False, 0)
        self.load_alerts()

    def load_suggested_packages(self):
        # Placeholder: Replace with dynamic loading of suggested packages
        suggested_packages = self.package_manager.get_suggested_packages()
        for package in suggested_packages:
            label = Gtk.Label(label=package)
            label.set_xalign(0)
            self.suggested_packages_box.pack_start(label, False, False, 0)
        self.suggested_packages_box.show_all()

    def load_alerts(self):
        # Placeholder: Replace with dynamic loading of alerts
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
        matched_packages = self.package_manager.search_packages(search_query)  # New method
        self.update_suggested_packages(matched_packages)

    def update_suggested_packages(self, packages):
        for child in self.suggested_packages_box.get_children():
            self.suggested_packages_box.remove(child)
        for package in packages:
            label = Gtk.Label(label=package)
            label.set_xalign(0)
            self.suggested_packages_box.pack_start(label, False, False, 0)
        self.suggested_packages_box.show_all()

