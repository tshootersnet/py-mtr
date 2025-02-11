# install_packages.py
import subprocess
import sys

def is_package_installed(package_name):
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def install_packages(packages):
    for package in packages:
        if not is_package_installed(package):
            print(f"'{package}' is not installed. Installing now...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"'{package}' installed successfully.")
        else:
            print(f"'{package}' is already installed.")

if __name__ == "__main__":
    packages = ["scapy", "tabulate"]
    install_packages(packages)
    print("Installation verification complete!")
