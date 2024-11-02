from src.utils.log_utils import tail_log

class LogHandler:
    def get_recent_logs(self, log_path="/var/log/emerge.log"):
        return tail_log(log_path)

