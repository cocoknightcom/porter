# src/ui/views/home_view.py
import os
from gi.repository import Gtk, Gdk
from src.controllers.package_manager import PackageManager

class HomeView(Gtk.Box):
    def __init__(self, parent):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.parent = parent
        self.package_manager = PackageManager()

        # Create a search bar with a rounded entry
        self.search_bar = Gtk.Entry()
        self.search_bar.set_placeholder_text("Search Packages")
        self.search_bar.set_property("width_chars", 30)
        self.search_bar.connect("activate", self.on_search_activated)
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

        # Create a ScrolledWindow for packages
        self.packages_scrolled_window = Gtk.ScrolledWindow()
        self.packages_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.packages_scrolled_window.add(self.packages_box)  # Add packages_box to the scrolled window
        self.pack_start(self.packages_scrolled_window, True, True, 0)
        
        self.horizontal_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)  # Create a box for the 3-columns layout
        self.packages_box.pack_start(self.horizontal_box, True, True, 0)  # Add to the main box
        self.current_row = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.horizontal_box.pack_start(self.current_row, True, True, 0)  # Start with the first column
        
        self.column_count = 0  # To track the current column
        
        self.load_installed_packages()  # Load installed packages when initialized

        # Notifications/Alerts section
        alerts_label = Gtk.Label(label="Notifications / Alerts")
        alerts_label.set_xalign(0)
        self.pack_start(alerts_label, False, False, 0)

        self.alerts_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.pack_start(self.alerts_box, False, False, 0)
        self.load_alerts()

    def load_installed_packages(self):
        # Fetch installed packages
        installed_packages = self.package_manager.get_installed_packages()
        for package in installed_packages:
            self.add_package_item(package)

    def add_package_item(self, package):
        """Create and add a package item to display."""
        # Create a vertical box for text
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        name_label = Gtk.Label(label=package["name"])
        description_label = Gtk.Label(label=package["description"])
        
        # Align text to the left
        name_label.set_xalign(0)
        description_label.set_xalign(0)

        vbox.pack_start(name_label, False, False, 0)
        vbox.pack_start(description_label, False, False, 0)

        # Create an image (icon)
        icon_image = Gtk.Image.new_from_file(package["icon"]) if os.path.exists(package["icon"]) else Gtk.Image.new_from_icon_name("package", Gtk.IconSize.DIALOG)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox.pack_start(icon_image, False, False, 0)
        hbox.pack_start(vbox, True, True, 0)

        # Use a 3-column layout inside the horizontal box
        if self.column_count < 3:
            self.current_column_box.pack_start(hbox, True, True, 0)  # Add to current column
            self.column_count += 1  # Move to the next column
        else:
            # If 3 columns are already there, create a new column
            self.current_column_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.horizontal_box.pack_start(self.current_column_box, True, True, 0)  # Add new column to horizontal box
            self.current_column_box.pack_start(hbox, True, True, 0)  # Add new package item to the new column
            self.column_count = 1  # Reset the column count
            
        self.packages_box.show_all()

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
        matched_packages = self.package_manager.search_packages(search_query)