import subprocess

def scan_ports(target):
    try:
        result = subprocess.run(
            ['nmap', '-Pn', '-T4', '-sV', '--top-ports', '1000', target],
            capture_output=True, text=True, timeout=900
        )
        return result.stdout.strip()
    except FileNotFoundError:
        return "nmap not installed, skipped"
    except subprocess.TimeoutExpired:
        return "nmap timed out"
    

    
