from modules.subdomain_enum import enumerate_subdomains
from modules.port_scanner import scan_ports
from modules.shodan_lookup import shodan_search
from modules.gpt_summarizer import summarize_recon
from dotenv import load_dotenv
from pyfiglet import figlet_format
from colorama import Fore, Style
import os
import json

load_dotenv()

def banner():
    print(Fore.CYAN + figlet_format("AI Recon Bot"))
    print(Fore.GREEN + "Automated Recon: Subdomains | Ports | Shodan | AI\n" + Style.RESET_ALL)

def main():
    banner()
    target = input(Fore.YELLOW + "[*] Enter domain or IP: " + Style.RESET_ALL)

    # Subdomain enumeration
    print(Fore.BLUE + "\n[+] Enumerating subdomains..." + Style.RESET_ALL)
    subdomains = enumerate_subdomains(target)
    if subdomains and subdomains[0] != "":
        print(Fore.WHITE + "\n".join(["  - " + sub for sub in subdomains]))
    else:
        print(Fore.WHITE + "  (No subdomains found)")

    # Port scanning (Nmap)
    print(Fore.BLUE + "\n[+] Scanning ports with Nmap..." + Style.RESET_ALL)
    port_results = scan_ports(target)
    print(Fore.WHITE + port_results)

    # Shodan lookup
    print(Fore.BLUE + "\n[+] Getting Shodan intel..." + Style.RESET_ALL)
    shodan_results = shodan_search(target)
    print(Fore.WHITE + json.dumps(shodan_results, indent=2))

    # Send everything to GPT
    print(Fore.MAGENTA + "\n[+] Sending all data to GPT..." + Style.RESET_ALL)
    recon_data = {
        "target": target,
        "subdomains": subdomains,
        "ports": port_results,
        "shodan": shodan_results
    }

    summary = summarize_recon(json.dumps(recon_data, indent=2))
    print(Fore.GREEN + "\n=== AI Recon Summary ===\n" + Style.RESET_ALL)
    print(summary)

if __name__ == "__main__":
    main()

