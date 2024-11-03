# src/controllers/package_manager.py
import subprocess
from src.utils.command_utils import run_command

class PackageManager:
    
    def get_installed_packages(self):
        """
        Retrieves explicitly user-installed packages from the @world set along with descriptions.
        Returns a list of dictionaries containing package name and description.
        """
        stdout, _ = run_command(["equery", "list", "@world"])
        packages = []
        
        for line in stdout.splitlines():
            package_name = line.strip()
            package_info = self.get_package_info(package_name)
            # Append only user-installed packages with their short descriptions
            packages.append({
                "name": package_name,
                "description": package_info["description"],  # Short description only
            })

        return packages

    def get_package_info(self, package_name):
        stdout, _ = run_command(["equery", "meta", package_name])
        # Here you can refine this to fetch only the description if the output includes more
        # Assuming the first line is the description
        description = stdout.splitlines()[0].strip() if stdout else "No description available"
        return {"name": package_name, "description": description}

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
