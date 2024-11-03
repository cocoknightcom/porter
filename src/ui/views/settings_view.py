# src/ui/views/settings_view.py
   from gi.repository import Gtk
   from src.controllers.config_manager import ConfigManager

   class SettingsView(Gtk.Box):
       def __init__(self, main_window):
           super().__init__(orientation=Gtk.Orientation.VERTICAL)
           self.main_window = main_window
           self.config_manager = ConfigManager()
           
           title_label = Gtk.Label(label="Settings")
           self.pack_start(title_label, False, False, 0)

           # Load settings
           self.load_settings()

           # Add a Button to save changes
           save_button = Gtk.Button(label="Save Changes")
           save_button.connect("clicked", self.save_changes)
           self.pack_start(save_button, False, False, 0)

       def load_settings(self):
           config_content = self.config_manager.read_config()
           self.config_text_view = Gtk.TextView()
           self.config_text_view.set_editable(True)  # Allow text editing
           self.config_text_view.get_buffer().set_text(config_content)  # Correctly set content
           self.pack_start(self.config_text_view, True, True, 0)

       def save_changes(self, widget):
           new_content = self.config_text_view.get_buffer().get_text(
               self.config_text_view.get_buffer().get_start_iter(),
               self.config_text_view.get_buffer().get_end_iter(),
               True
           )
           self.config_manager.write_config(new_content)