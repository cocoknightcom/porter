# src/utils/command_utils.py
import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return "", str(e)