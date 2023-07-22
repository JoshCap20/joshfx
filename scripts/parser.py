import requests
from bs4 import BeautifulSoup
import csv
import os
import re
from urllib.parse import urljoin, urlparse, unquote
from scripts.proxy import proxy_request

class Scraper:
    visited = set()
    pattern = re.compile(r'(.*/S\d+/)([\w\.]+).S(\d+)E(\d+)')
    sources: list[str] = [
        "http://102.212.178.1:8089/",
        "http://185.223.160.51/",
        "http://192.121.102.206/",
        "http://92.247.236.71:9800/",
        "http://66.242.75.177/",
        "http://195.154.237.18:9000/",
        "http://210.54.35.157:9000/",
        "http://124.184.68.140/",
        "http://195.154.108.130:9000/",
        "http://120.28.137.252/",
        "http://144.137.208.140:9000/",
        "http://72.253.204.218:9999/movies/",
        "http://96.233.113.244/",
        "http://23.147.64.113/",
    ]

    @classmethod
    def scrape(self) -> None:
        for source in self.sources:
            self.find_videos(source)

    @classmethod
    def find_videos(self, base_url, path='') -> None:
        page_url = urljoin(base_url, path)

        if page_url in self.visited:
            return
        self.visited.add(page_url)
        response = requests.get(page_url)
        # response = proxy_request(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a'):
            href = link.get('href')

            if not any(href.endswith(ext) for ext in ['.mp4', '.mkv']):
                continue

            video_url = urljoin(page_url, href)
            path = urlparse(video_url).path
            directory = os.path.dirname(path)
            title = os.path.basename(path)
            
            title = unquote(title)
            full_path = os.path.join(directory, title)
            match = self.pattern.search(full_path)

            if match:
                show_name = match.group(2).replace('.', ' ')
                season = match.group(3)
                episode = match.group(4)
                title = f"{show_name} S{season}E{episode}"
            else:
                title = os.path.basename(directory)
                title = unquote(title)

            with open('video32.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([title, video_url, base_url])

        # Recursively visit each directory
        for link in soup.find_all('a'):
            href = link.get('href')

            if not href.endswith('/'):
                continue

            self.find_videos(base_url, os.path.join(path, href))

    

# base_url = 'http://102.212.178.1:8089/'
# find_videos(base_url)
