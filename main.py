from modules.subdomain_enum import enumerate_subdomains
from modules.port_scanner import scan_ports
from modules.shodan_lookup import shodan_search
from modules.http_probe import probe_hosts
from modules.gpt_summarizer import summarize_recon
from modules.validate import is_valid_target
from dotenv import load_dotenv
from pyfiglet import figlet_format
from colorama import Fore, Style
from datetime import datetime
import argparse
import os
import sys
import json

load_dotenv()

def banner():
    print(Fore.CYAN + figlet_format("AI Recon Bot"))
    print(Fore.GREEN + "Automated Recon: Subdomains | Ports | Shodan | AI\n" + Style.RESET_ALL)

def parse_args():
    p = argparse.ArgumentParser(description="AI Recon Bot")
    p.add_argument("-t", "--target", help="domain or IP (prompted if omitted)")
    p.add_argument("--skip-ports", action="store_true", help="skip the nmap scan")
    p.add_argument("--skip-shodan", action="store_true", help="skip the Shodan lookup")
    p.add_argument("-o", "--output-dir", default="reports", help="report directory")
    return p.parse_args()

def main():
    args = parse_args()
    banner()
    target = (args.target or input(Fore.YELLOW + "[*] Enter domain or IP: " + Style.RESET_ALL)).strip()
    if not is_valid_target(target):
        sys.exit(Fore.RED + f"[!] '{target}' is not a valid domain or IP" + Style.RESET_ALL)

    # Subdomain enumeration
    print(Fore.BLUE + "\n[+] Enumerating subdomains..." + Style.RESET_ALL)
    subdomains = enumerate_subdomains(target)
    if subdomains and subdomains[0] != "":
        print(Fore.WHITE + "\n".join(["  - " + sub for sub in subdomains]))
    else:
        print(Fore.WHITE + "  (No subdomains found)")

    # Port scanning (Nmap)
    print(Fore.BLUE + "\n[+] Scanning ports with Nmap..." + Style.RESET_ALL)
    port_results = "skipped" if args.skip_ports else scan_ports(target)
    print(Fore.WHITE + port_results)

    # HTTP probe
    print(Fore.BLUE + "\n[+] Probing live web hosts..." + Style.RESET_ALL)
    web_hosts = [s for s in subdomains if s and not s.startswith("Error")] or [target]
    http_results = probe_hosts(web_hosts)
    for h in http_results:
        print(Fore.WHITE + f"  {h['url']} [{h['status']}] {h['server']} {h['title']}")
        if h["missing_headers"]:
            print(Fore.YELLOW + "    missing: " + ", ".join(h["missing_headers"]) + Style.RESET_ALL)
    if not http_results:
        print(Fore.WHITE + "  (No live web hosts)")

    # Shodan lookup
    print(Fore.BLUE + "\n[+] Getting Shodan intel..." + Style.RESET_ALL)
    shodan_results = [] if args.skip_shodan else shodan_search(target)
    print(Fore.WHITE + json.dumps(shodan_results, indent=2))

    # Send everything to GPT
    print(Fore.MAGENTA + "\n[+] Sending all data to GPT..." + Style.RESET_ALL)
    recon_data = {
        "target": target,
        "subdomains": subdomains,
        "ports": port_results,
        "http": http_results,
        "shodan": shodan_results
    }

    summary = summarize_recon(json.dumps(recon_data, indent=2))
    print(Fore.GREEN + "\n=== AI Recon Summary ===\n" + Style.RESET_ALL)
    print(summary)

    report = {
        "timestamp": datetime.now().isoformat(),
        "target": target,
        "subdomains": subdomains,
        "ports": port_results,
        "http": http_results,
        "shodan": shodan_results,
        "ai_summary": summary
    }

    os.makedirs(args.output_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(args.output_dir, f"recon_{target.replace('.', '_')}_{stamp}.json")
    with open(filename, "w") as f:
        json.dump(report, f, indent=2)

    print(Fore.CYAN + f"\n[+] Report saved to {filename}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()

