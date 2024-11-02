import os

def tail_log(file_path, lines=10):
    """Read the last `lines` lines from the specified log file."""
    if not os.path.isfile(file_path):
        return []

    with open(file_path, 'rb') as f:
        # Move to the end of the file and read backwards
        f.seek(0, os.SEEK_END)
        buffer = bytearray()
        end_char_count = 0

        while len(buffer) < 1024 * lines and f.tell() > 0:
            f.seek(-1, os.SEEK_CUR)
            char = f.read(1)
            f.seek(-1, os.SEEK_CUR)
            
            if char == b'\n':
                end_char_count += 1
                if end_char_count == lines + 1:  # +1 to skip the final newline
                    break
            buffer.extend(char)
        
        # Decode bytes and split lines, reversing order
        return buffer[::-1].decode(errors='ignore').strip().splitlines()[::-1]

def log_message(message):
    """Format a log message to standard output."""
    print(f"[PORTER LOG] {message}")

