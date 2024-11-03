# src/controllers/package_manager.py
import subprocess
from src.utils.command_utils import run_command

class PackageManager:
    
    def get_installed_packages(self):
        """
        Retrieves installed packages from the @world set along with descriptions.
        Returns a list of dictionaries containing package name, description, and icon path.
        """
        stdout, _ = run_command(["equery", "list", "@world"])
        packages = []
        
        for line in stdout.splitlines():
            package_name = line.strip()
            package_info = self.get_package_info(package_name)
            icon_path = f"icons/{package_name}.png"  # Example path for icons
            packages.append({
                "name": package_name,
                "description": package_info["description"],
                "icon": icon_path
            })

        return packages

    def get_package_info(self, package_name):
        stdout, _ = run_command(["equery", "meta", package_name])
        info = {"name": package_name, "description": stdout.strip()}
        return info
    def get_suggested_packages(self):
        """
        Retrieve a list of suggested packages based on popularity or recent installs.
        This is a placeholder and could be enhanced by actual data on popular packages.
        """
        # Placeholder approach: Using a hardcoded list of popular packages for now.
        # For a dynamic solution, integrate with a package popularity service or analyze installed packages.

        suggested_packages = [
            "vim", "git", "htop", "curl", "gcc", "python", "nodejs", 
            "docker", "nginx", "postgresql", "tmux", "zsh"
        ]

        # To get actual data on recent installs or most-used packages, you could:
        # 1. Parse logs
        # 2. Query a Gentoo-specific popularity service or package index (if available)
        # 3. Use other package metadata (future scope)

        return suggested_packages

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
