import subprocess

def scan_ports(target):
    try:
        result = subprocess.run(
            ['nmap', 'Pn', 'T4', '-sVT', '1000', target],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error; {e}"
    

    
