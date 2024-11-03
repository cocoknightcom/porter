# src/controllers/package_manager.py
import subprocess
from src.utils.command_utils import run_command

class PackageManager:
    
    def get_installed_packages(self):
        packages = []
        
        default_icon_path = "/path/to/default/icon.png"  # Replace with actual default icon path

        stdout, _ = run_command(["equery", "list", "@world"])
        
        for line in stdout.splitlines():
            package_name = line.strip()
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

        # Get package name
        stdout, stderr = run_command(["eix", "-I", package_name, "--format", "<name>"])
        if stdout.strip():  # Check if there is output
            package_info["name"] = stdout.strip()
        else:
            package_info["name"] = "Unknown"

        # Get package description
        stdout, stderr = run_command(["eix", "-I", package_name, "--format", "<description>"])
        if stdout.strip():
            package_info["description"] = stdout.strip()
        else:
            package_info["description"] = "No description available"

        # Get package category/name
        stdout, stderr = run_command(["eix", "-I", package_name, "--format", "<category>/<name>"])
        if stdout.strip():
            package_info["category"] = stdout.strip()
        else:
            package_info["category"] = "Unknown"

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
