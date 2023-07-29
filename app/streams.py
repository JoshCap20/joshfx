import re
from wsgiref.util import FileWrapper

import requests
from django.http import StreamingHttpResponse
from urllib3.exceptions import ProtocolError


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

    resp = requests.get(url, headers=headers, stream=True, timeout=(10, 30))

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
