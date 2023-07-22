import requests
import random
import json

with open('proxies.json') as f:
    data = json.load(f)

def proxy_request(url, request_type = "get", **kwargs):
    while True:
        try:
            item = random.choice(data)
            ip = item['ip']
            port = item['port']
            protocol = item['protocols'][0]  # select the first protocol

            proxy = f"{protocol}://{ip}:{port}"
            proxies = {"http": proxy, "https": proxy}

            if request_type.lower() == "get":
                response = requests.get(url, proxies=proxies, **kwargs)
            elif request_type.lower() == "post":
                response = requests.post(url, proxies=proxies, **kwargs)
            else:
                raise ValueError("Invalid request_type. Choose either 'get' or 'post'")
                
            print(f"Proxy currently being used: {proxy}")
            break
        except:
            print("Error, looking for another proxy")
    return response