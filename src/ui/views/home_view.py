# src/ui/views/home_view.py
import os
from gi.repository import Gtk, Gdk, GLib
from src.controllers.package_manager import PackageManager
from src.ui.views.log_view import LogView

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
        self.packages_box = Gtk.Grid()
        self.packages_box.set_column_spacing(10)
        self.packages_box.set_row_spacing(10)
        self.packages_scrolled_window.add(self.packages_box)
        self.pack_start(self.packages_scrolled_window, True, True, 0)

        # Loading spinner now only managed on package loading
        self.loading_spinner = Gtk.Spinner()
        self.loading_spinner.set_margin_top(20)
        self.pack_start(self.loading_spinner, True, False, 0)  # Pack the spinner initially
        self.load_installed_packages()  # Load installed packages when initialized

        # Notifications/Alerts section
        alerts_label = Gtk.Label(label="Notifications / Alerts")
        alerts_label.set_xalign(0)
        self.pack_start(alerts_label, False, False, 0)

        self.alerts_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.pack_start(self.alerts_box, False, False, 0)
        self.load_alerts()

    def show_loading_spinner(self):
        if not self.loading_spinner.get_visible():
            self.loading_spinner.set_property("visible", True)  # Show spinner
            self.pack_start(self.loading_spinner, True, False, 0)  # Ensure spinner is visible in layout
            self.loading_spinner.start()  # Start the spinner

    def hide_loading_spinner(self):
        self.loading_spinner.stop()  # Stop the spinner
        self.loading_spinner.set_property("visible", False)  # Hide spinner
        if self.loading_spinner in self.get_children():
            self.remove(self.loading_spinner)  # Remove spinner from the view
        
    def load_installed_packages(self):
        self.show_loading_spinner()
        GLib.idle_add(self._load_installed_packages_background)

    def _load_installed_packages_background(self):
        installed_packages = self.package_manager.get_installed_packages()
        for index, package in enumerate(installed_packages):
            GLib.idle_add(self.add_package_item, package, index)
            
        self.hide_loading_spinner()
        return False  # Stop calling this function

    def add_package_item(self, package, index):
        """Create and add a package item to display."""
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        
        # Set name as a title (bold) and description as normal text
        name_label = Gtk.Label(label=package["name"])  # Only display the package name as title
        description_label = Gtk.Label(label=f"{package['description']}\n<small>{package['category']}</small>")  # Updated category info

        name_label.set_use_markup(True)  # Enable markup for formatting
        name_label.set_label(f"<b>{package['name']}</b>")  # Keep it as bold
        description_label.set_use_markup(True)  # Enable markup for formatting
        
        # Align text to the left
        name_label.set_xalign(0)
        description_label.set_xalign(0)

        vbox.pack_start(name_label, False, False, 0)
        vbox.pack_start(description_label, False, False, 0)

        icon_image = Gtk.Image.new_from_file(package["icon"]) if os.path.exists(package["icon"]) else Gtk.Image.new_from_icon_name("package", Gtk.IconSize.DIALOG)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox.pack_start(icon_image, False, False, 0)
        hbox.pack_start(vbox, True, True, 0)

        row = index // 3  # Calculate the row based on the index
        col = index % 3   # Calculate the column based on the index
        self.packages_box.attach(hbox, col, row, 1, 1)  # Add to the grid

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
        success = self.package_manager.sync_portage()
        if success:
            print("Portage synced successfully.")
            self.alerts_box.pack_start(Gtk.Label(label="Portage sync completed successfully."), False, False, 0)
            self.log_view.refresh_logs()  # Refresh logs
        else:
            print("Failed to sync Portage.")
            self.alerts_box.pack_start(Gtk.Label(label="Failed to sync Portage. Please check the logs."), False, False, 0)
        self.alerts_box.show_all()  # Make sure to refresh UI to show alert messages

    def on_view_installed_clicked(self, widget):
        print("View Installed Packages clicked")

    def on_view_categories_clicked(self, widget):
        print("View Categories clicked")
    
    def on_search_activated(self, entry):
        search_query = self.search_bar.get_text()
        if search_query:  # Ensure not empty
            matched_packages = self.package_manager.search_packages(search_query)
            self.update_package_grid(matched_packages)
    
    def update_package_grid(self, packages):
        # Clear current packages in the display
        self.packages_box.foreach(lambda widget: self.packages_box.remove(widget))
        for index, package in enumerate(packages):
            self.add_package_item(package, index)