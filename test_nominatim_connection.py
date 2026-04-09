
import requests

def test_connection():
    url = 'https://nominatim.openstreetmap.org/search'
    params = {'q': 'Coventry', 'format': 'json'}
    headers = {'User-Agent': 'GeoMapper-Test-Script'}
    
    print(f"Testing connection to {url}...")
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response snippet:", response.text[:200])
        else:
            print("Failed to get 200 OK")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()
