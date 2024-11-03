# src/ui/views/log_view.py
from gi.repository import Gtk
from src.controllers.log_handler import LogHandler

class LogView(Gtk.Box):
    def __init__(self, parent):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.parent = parent
        self.log_handler = LogHandler()

        self.text_view = Gtk.TextView()
        self.text_view.set_editable(False)
        self.pack_start(self.text_view, True, True, 0)

        self.refresh_logs()

    def refresh_logs(self):
        log_content = self.log_handler.get_recent_logs()
        
        # Join the list into a single string, with each line separated by a newline
        log_content_str = "\n".join(log_content)
        
        buffer = self.text_view.get_buffer()
        buffer.set_text(log_content_str)
