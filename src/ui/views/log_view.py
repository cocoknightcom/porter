# src/ui/views/log_view.py
from gi.repository import Gtk
from src.controllers.log_handler import LogHandler

class LogView(Gtk.Box):
    def __init__(self, parent):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.parent = parent
        self.log_handler = LogHandler()

        # Create a TextView and its buffer
        self.text_view = Gtk.TextView()
        self.text_view.set_editable(False)
        self.pack_start(self.text_view, True, True, 0)

        # Initialize the TextBuffer to manage the content of the TextView
        self.text_buffer = self.text_view.get_buffer()
        
        self.refresh_logs()

    def refresh_logs(self):
        log_content = self.log_handler.get_recent_logs()
        
        # Join the list into a single string, with each line separated by a newline
        log_content_str = "\n".join(log_content)
        
        # Use the text buffer to set the text in the TextView
        self.text_buffer.set_text(log_content_str)