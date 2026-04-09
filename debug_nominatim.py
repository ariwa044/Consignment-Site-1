
import requests
import socket
import json

def debug_connection():
    domain = 'nominatim.openstreetmap.org'
    url = f'https://{domain}/search'
    
    print(f"--- Debugging Connection to {domain} ---")
    
    # 1. DNS Resolution
    print(f"\n[Step 1] Resolving DNS for {domain}...")
    try:
        ip_list = socket.getaddrinfo(domain, 443)
        print("Resolved IPs:")
        seen_ips = set()
        for res in ip_list:
            ip = res[4][0]
            if ip not in seen_ips:
                print(f"  - {ip}")
                seen_ips.add(ip)
    except Exception as e:
        print(f"DNS Resolution failed: {e}")

    # 2. Test with default requests User-Agent
    print(f"\n[Step 2] Request with default User-Agent...")
    try:
        r = requests.get(url, params={'q': 'London', 'format': 'json'}, timeout=5)
        print(f"Status: {r.status_code}")
    except Exception as e:
        print(f"Failed: {e}")

    # 3. Test with Browser User-Agent
    print(f"\n[Step 3] Request with Browser User-Agent...")
    browser_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    try:
        r = requests.get(url, params={'q': 'London', 'format': 'json'}, headers={'User-Agent': browser_ua}, timeout=5)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print("Success! It might be a User-Agent issue.")
        else:
            print("Still failed.")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    debug_connection()
