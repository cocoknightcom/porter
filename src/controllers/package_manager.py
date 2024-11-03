# src/controllers/package_manager.py
import subprocess
from src.utils.command_utils import run_command

class PackageManager:
    
    def get_installed_packages(self):
        packages = []

        default_icon_path = "/path/to/default/icon.png"  # Replace with actual default icon path

        # Read package names from /var/lib/portage/world
        with open("/var/lib/portage/world", "r") as f:
            package_names = f.read().splitlines()

        for package_name in package_names:
            package_info = self.get_package_info(package_name)

            # Append only user-installed packages with their short descriptions, category, and an icon
            packages.append({
                "name": package_info["name"],
                "description": package_info["description"],  # Short description only
                "category": package_info["category"],  # Include category
                "icon": default_icon_path  # Add icon path here
            })

        return packages

    def get_package_info(self, package_name):
        package_info = {}
        
        # Get package info using a more refined format specification
        stdout, stderr = run_command(["eix", "-I", package_name, "--format", "<name> [<version>] - <description> (<category>)"])
        if stdout.strip():
            # Split output into lines and take the first match
            package_lines = stdout.strip().splitlines()
            first_match = package_lines[0].split(" - ")
            if len(first_match) == 2:
                # Extract name, version, description, and category correctly
                name_version = first_match[0].split("[")
                package_info["name"] = name_version[0].strip()
                package_info["version"] = name_version[1].rstrip("]") if len(name_version) > 1 else "Unknown"
                package_info["description"], category_info = first_match[1].strip().split(" (")
                package_info["category"] = category_info.rstrip(")")  # Remove the closing parenthesis
            else:
                package_info["name"] = "Unknown"
                package_info["description"] = "No description available"
                package_info["category"] = "Unknown"
                package_info["version"] = "Unknown"
        else:
            package_info["name"] = "Unknown"
            package_info["description"] = "No description available"
            package_info["category"] = "Unknown"
            package_info["version"] = "Unknown"

        return package_info

    def install_package(self, package_name):
        """
        Installs a package using emerge.
        """
        try:
            subprocess.run(["sudo", "emerge", package_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error installing package {package_name}: {e}")

    def remove_package(self, package_name):
        """
        Removes a package using emerge.
        """
        try:
            subprocess.run(["sudo", "emerge", "--unmerge", package_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error removing package {package_name}: {e}")
            
    def search_packages(self, query):
        """
        Search for packages matching the query using `equery` for localinstalled packages.
        Returns a list of package names that match the query.
        """
        stdout, _ = run_command(["equery", "list", query])
        return stdout.splitlines()
