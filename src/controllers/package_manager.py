# src/controllers/package_manager.py
import subprocess
from src.utils.command_utils import run_command

class PackageManager:
    
    def get_installed_packages(self):
        packages = []
        
        # For simplicity, setting a default icon for each package
        default_icon_path = "/path/to/default/icon.png"  # Replace with actual default icon path

        # The rest of the code remains the same
        stdout, _ = run_command(["equery", "list", "@world"])
        
        for line in stdout.splitlines():
            package_name = line.strip()
            package_info = self.get_package_info(package_name)

            # Append only user-installed packages with their short descriptions and an icon
            packages.append({
                "name": package_name,
                "description": package_info["description"],  # Short description only
                "icon": default_icon_path  # Add icon path here
            })

        return packages

    def get_package_info(self, package_name):
        stdout, _ = run_command(["equery", "meta", package_name])
        if stdout:
            lines = stdout.splitlines()
            description = lines[0].strip() if len(lines) > 0 else "No description available"
            category = package_name.split('/')[0]  # Assuming that package_name is of the format 'category/name'
            return {"name": package_name, "description": description, "category": category}
        return {"name": package_name, "description": "No description available", "category": "Unknown"}

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
