import csv
import os
import re
from urllib.parse import unquote, urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from scripts.proxies import get_random_proxy_dict

# from scripts.proxy import proxy_request


class Scraper:
    visited = set()
    output_file = 'output.csv'

    sources: list[str] = [
        "http://102.212.178.1:8089/",
        "http://185.223.160.51/",
        "http://192.121.102.206/",
        "http://66.242.75.177/",
        "http://96.233.113.244/",
        "http://195.154.237.18:9000/",
        "http://23.147.64.113/",
        "http://124.184.68.140/",
        
        # HAVENT TESTED BELOW
        
        "https://didi2.ir/bestsitcomdl/",
        # "http://210.54.35.157:9000/",
        # "http://144.137.208.140:9000/",
        # "http://72.253.204.218:9999/movies/",
        # "http://92.247.236.71:9800/" # Doesn't load
        # "http://195.154.108.130:9000/", # Not Interesting
        # "http://120.28.137.252/", # Not Interesting
    ]

    @classmethod
    def scrape(cls) -> None:
        for source in cls.sources:
            cls.find_videos(source)

    @classmethod
    def __get_pattern(cls, source: str) -> re.Pattern:
        if cls.sources[0] == source:
            return re.compile(r'(.*/S\d+/)([\w\.]+).S(\d+)E(\d+)')
        elif cls.sources[1] == source:
            # return re.compile(r'(.*/)([\w\.\-\']+)[._](\d{4}).*')
            return re.compile(r'(.*/)([\w\.\-\']+)[._](\d{3,4})[._]?(\w*p)?[._]?.*')
        elif cls.sources[2] == source:
            return re.compile(r'(/)?(([\w\.\%]+)[._](\d{4}|S\d+E\d+)[._]?(.*))\.(mkv|mp4)$')
        elif cls.sources[3] == source:
            return re.compile(r"/tv/(.*?)/Season.*?/(.*?) - (S\d{2}E\d{2})")
        elif cls.sources[4] == source:
            # return re.compile(r'/TV/([^/]+)/Season\s+(\d+)/([^/]+) S(\d+)E(\d+) ')
            return re.compile(r'\/TV\/([^\/]+)\/Season( |%20)(\d+)\/[^\/]+ S(\d+)E(\d+)')
        return re.compile(r'(.*/S\d+/)([\w\.]+).S(\d+)E(\d+)')

    @classmethod
    def __extract_pattern(cls, source, match):
        if cls.sources[0] == source:
            show_name = match.group(2).replace(
                '.', ' ') if match.group(2) else ''
            season = f"S{match.group(3)}" if len(
                match.groups()) >= 3 and match.group(3) else ''
            episode = f"E{match.group(4)}" if len(
                match.groups()) >= 4 and match.group(4) else ''
            return f"{show_name} {season}{episode}"
        elif cls.sources[1] == source:
            show_name = match.group(2).replace(
                '.', ' ') if match.group(2) else ''
            year = f"({match.group(3)})" if len(match.groups()) >= 3 and match.group(
                3) and match.group(3) not in ["1400", "800", "MB", "mb"] else ''
            quality = f"({match.group(4)})" if len(match.groups()) >= 4 and match.group(
                4) and match.group(4) not in ["mp4", "mkv"] else ''
            return f"{show_name} {year} {quality}"
        elif cls.sources[2] == source:
            title = match.group(2).replace('.', ' ').replace(
                '%20', ' ') if match.group(2) else ''
            year_or_season_episode = match.group(4) if match.group(4) else ''
            return f"{title} {year_or_season_episode}"
        elif cls.sources[3] == source:
            title = re.sub('%20', ' ', match.group(1))
            if "%27" in title:
                title = re.sub('%27', '\'', title)
            season_episode = match.group(3)
            return f"{title} - {season_episode}"
        elif cls.sources[4] == source:
            show_title = match.group(1).replace('%20', ' ')
            if "%27" in show_title:
                show_title = re.sub('%27', '\'', show_title)
            season = match.group(4)
            episode = match.group(5)
            return f"{show_title}, S{season}E{episode}"

        show_name = match.group(2).replace('.', ' ') if match.group(2) else ''
        season = f"S{match.group(3)}" if len(
            match.groups()) >= 3 and match.group(3) else ''
        episode = f"E{match.group(4)}" if len(
            match.groups()) >= 4 and match.group(4) else ''
        return f"{show_name} {season}{episode}"

    @classmethod
    def find_videos(cls, base_url, path='') -> None:
        pattern = cls.__get_pattern(base_url)
        page_url = urljoin(base_url, path)

        if page_url in cls.visited:
            return
        cls.visited.add(page_url)
        try:
            response = requests.get(page_url, timeout=(20, 40), proxies=get_random_proxy_dict())
        except requests.exceptions.Timeout:
            print(f"Timed out: {page_url}")
            return
        except requests.exceptions.ConnectionError:
            # Need better error handling in future
            try:
                response = requests.get(page_url, timeout=(20, 40))
            except:
                print(f"Connect error: {page_url}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return
        except Exception as e:
            print(f"Unknown error: {e}")
            return

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
            print("FULL " + full_path)
            match = pattern.search(full_path)

            if match:
                title = cls.__extract_pattern(base_url, match)
            else:
                if base_url in cls.sources[6:8]:
                    title = os.path.basename(path)
                    title = unquote(title)
                else:
                    title = os.path.basename(directory)
                    title = unquote(title)

            print(f"Found: {title} {video_url} {base_url} {path}")

            with open(cls.output_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([title, video_url, base_url, path])

        # Recursively visit each directory
        for link in soup.find_all('a'):
            href = link.get('href')

            if not href.endswith('/'):
                continue

            # if path.startswith("/"):
            #     path = path[1:]

            # cls.find_videos(base_url, os.path.join(path, href))
            cls.find_videos(base_url, urljoin(path, href))


if __name__ == "__main__":
    Scraper.scrape()

# base_url = 'http://102.212.178.1:8089/'
# find_videos(base_url)
