import os

def read_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            return file.read()
    return ""

def write_file(filepath, content):
    with open(filepath, "w") as file:
        file.write(content)

