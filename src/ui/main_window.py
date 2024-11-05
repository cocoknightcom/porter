# src/ui/main_window.py
from gi.repository import Gtk, GLib
from src.ui.views.home_view import HomeView
from src.ui.views.package_detail import PackageDetailView
from src.ui.views.log_view import LogView
from src.ui.views.settings_view import SettingsView

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Porter - Gentoo Package Manager GUI")

        # Initialize views
        self.home_view = HomeView(self)
        self.package_detail_view = PackageDetailView(self)
        self.log_view = LogView(self)
        self.settings_view = SettingsView(self)

        # Add views to stack
        self.stack.add_titled(self.home_view, "home", "Home")
        self.stack.add_titled(self.package_detail_view, "package_detail", "Package Detail")
        self.stack.add_titled(self.log_view, "log", "Logs")
        self.stack.add_titled(self.settings_view, "settings", "Settings")

        # Layout
        vbox = Gtk.VBox()
        vbox.pack_start(self.stack_switcher, False, False, 0)
        vbox.pack_start(self.stack, True, True, 0)
        self.add(vbox)
        
        # Show the home view by default
        self.stack.set_visible_child(self.home_view)
        
    def navigate_to(self, view_name):
        if view_name == "home":
            self.stack.set_visible_child(self.home_view)
        elif view_name == "package_detail":
            self.stack.set_visible_child(self.package_detail_view)
        elif view_name == "log":
            self.stack.set_visible_child(self.log_view)
        elif view_name == "settings":
            self.stack.set_visible_child(self.settings_view)

