import subprocess

def enumerate_subdomains(domain):
    try:
        result = subprocess.run(
            ['subfinder', '-d', domain, '-silent'],
            capture_output=True, text=True
        )
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"Error:{e}"]
    
    
