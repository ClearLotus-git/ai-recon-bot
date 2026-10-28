# AI Recon Bot (NS3D Framework)

An AI-powered modular recon tool that automates the enumeration of subdomains, ports, Shodan data, and summarizes it using GPT.

##  Features

- Subdomain Enumeration (Subfinder)
- Port Scanning (Nmap)
- HTTP Probe (status, server, title, missing security headers)
- Shodan Intelligence (optional, API key required)
- AI Recon Summary (OpenAI GPT)
- Modular, CLI-based, and extensible

##  Installation

```bash
git clone https://github.com/yourusername/ai-recon-bot.git
cd ai-recon-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## How to Run

```bash
python3 main.py -t example.com
python3 main.py -t example.com --skip-ports --skip-shodan -o out
```

Run without `-t` to be prompted for a target. Reports are saved as timestamped JSON in `reports/`.







