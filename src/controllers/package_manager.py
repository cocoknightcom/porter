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

        # Get package name
        stdout, stderr = run_command(["eix", "-I", package_name, "--format", "<name>", "--selected-file"])
        if stdout.strip():  # Check if there is output
            package_info["name"] = stdout.strip().split('[1]')[0]
        else:
            package_info["name"] = "Unknown"

        # Get package description
        stdout, stderr = run_command(["eix", "-I", package_name, "--format", "<description>", "--selected-file"])
        if stdout.strip():
            package_info["description"] = stdout.strip().split('[1]')[0]
        else:
            package_info["description"] = "No description available"

        # Get package category/name
        stdout, stderr = run_command(["eix", "-I", package_name, "--format", "<category>/<name>", "--selected-file"])
        if stdout.strip():
            package_info["category"] = stdout.strip().split('[1]')[0]
        else:
            package_info["category"] = "Unknown"

        return package_info

    def install_package(self, package_name):
        try:
            stdout, stderr = run_command(["emerge", package_name])
            return stdout, stderr  # Return output for logging or UI feedback
        except Exception as e:
            print(f"Error installing package {package_name}: {e}")
            return None, str(e)

    def remove_package(self, package_name):
        try:
            stdout, stderr = run_command(["emerge", "--unmerge", package_name])
            return stdout, stderr  # Return output for logging or UI feedback
        except Exception as e:
            print(f"Error removing package {package_name}: {e}")
            return None, str(e)
            
    def search_packages(self, query):
        """
        Search for packages matching the query using `equery` for localinstalled packages.
        Returns a list of package names that match the query.
        """
        stdout, _ = run_command(["equery", "list", query])
        return stdout.splitlines()
    def sync_portage(self):
        """
        Sync the Portage tree using emerge --sync.
        """
        try:
            subprocess.run(["emerge", "--sync"], check=True)
            return True  # Indicate success
        except subprocess.CalledProcessError as e:
            print(f"Error syncing Portage: {e}")
            return False  # Indicate failure
    def get_use_flags(self, package_name):
        """
        Get USE flags for a given package using equery.
        """
        stdout, _ = run_command(["equery", "use", package_name])
        return stdout.splitlines()

    def toggle_use_flag(self, package_name, flag_name, enable):
        """
        Toggle a USE flag for a specified package.
        """
        action = 'set' if enable else 'unset'
        try:
            subprocess.run(["sudo", "equery", action, flag_name, package_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error toggling USE flag {flag_name} for package {package_name}: {e}")
    def get_pending_updates(self):
        if stdout:
            return stdout.splitlines()  # Returns lines indicating updates available
        else:
            return ["No pending updates."]