import re
import time
from wsgiref.util import FileWrapper

import requests
from django.http import StreamingHttpResponse
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException
from urllib3.util.retry import Retry
from urllib3.exceptions import ProtocolError

from scripts.proxies import get_random_proxy_dict, get_random_user_agent


def stream_external_video(movie):
    response = requests.get(movie.link, stream=True)

    def generate():
        for chunk in response.iter_content(chunk_size=4096):
            yield chunk

    return StreamingHttpResponse(generate(), content_type='video/mp4')


def stream_external_video_adv(movie, request):
    url = movie.link

    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = re.match(r'bytes=(\d+)-(\d+)?', range_header)

    if range_match is None:
        headers = {}
        status_code = 200
    else:
        start, end = range_match.groups()
        if end is None:
            # No end, get the rest of the file
            headers = {"Range": f"bytes={start}-"}
        else:
            headers = {"Range": f"bytes={start}-{end}"}
        status_code = 206

    # headers["User-Agent"] = get_random_user_agent()

    # session = requests.Session()
    # retry = Retry(total=3, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
    # adapter = HTTPAdapter(max_retries=retry)
    # session.mount('http://', adapter)
    # session.mount('https://', adapter)

    # try:
    #     resp = session.get(url, headers=headers, stream=True, timeout=(10, 30), proxies=get_random_proxy_dict())
    # except RequestException as e:
    #     print(f"Request failed: {e}")
    #     return
    
    headers["User-Agent"] = get_random_user_agent()
    session = requests.Session()
    max_retries = 3

    for attempt in range(max_retries):
        try:
            resp = session.get(url, headers=headers, stream=True, timeout=(10, 30), proxies=get_random_proxy_dict())
            break
        except RequestException as e:
            print(f"Request failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(0.1 * (2 ** attempt))
            else:
                return 


    try:
        response = StreamingHttpResponse(
            FileWrapper(resp.raw),
            status=status_code,
            content_type='video/mp4'
        )
    except ProtocolError as e:
        print(f"Stream was interrupted: {e}")

    if 'Content-Range' in resp.headers:
        response['Content-Range'] = resp.headers['Content-Range']
    response['Accept-Ranges'] = 'bytes'

    return response
