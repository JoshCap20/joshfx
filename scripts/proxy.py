import requests
import random
import json

with open('proxies.json') as f:
    data = json.load(f)

ip_addresses = [f"{item['ip']}:{item['port']}" for item in data]    

def proxy_request(request_type, url, **kwargs):
    while True:
        try:
            proxy = random.choice(ip_addresses)
            proxies = {"http": proxy, "https": proxy}
            if request_type.lower() == "get":
                response = requests.get(url, proxies=proxies, timeout=5, **kwargs)
            elif request_type.lower() == "post":
                response = requests.post(url, proxies=proxies, timeout=5, **kwargs)
            else:
                raise ValueError("Invalid request_type. Choose either 'get' or 'post'")
                
            print(f"Proxy currently being used: {proxy}")
            break
        except:
            print("Error, looking for another proxy")
    return response