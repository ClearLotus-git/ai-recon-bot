import subprocess

def enumerate_subdomains(domain):
    try:
        result = subprocess.run(
            ['subfinder', '-d', domain, '-silent'],
            capture_output=True, text=True, timeout=300
        )
    except FileNotFoundError:
        print("  subfinder not installed, skipping")
        return []
    except subprocess.TimeoutExpired:
        print("  subfinder timed out")
        return []
    return [s for s in result.stdout.splitlines() if s.strip()]
    
    
