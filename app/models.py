import os
import subprocess
from django.db import models
from django.http import StreamingHttpResponse
import requests
from wsgiref.util import FileWrapper
import re
from urllib3.exceptions import ProtocolError

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    path = models.CharField(max_length=200)
    type = models.CharField(max_length=30)
    link = models.CharField(max_length=200)
    source = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
    def stream_external_video(self):
      response = requests.get(self.link, stream=True)

      def generate():
          for chunk in response.iter_content(chunk_size=4096):
              yield chunk

      return StreamingHttpResponse(generate(), content_type='video/mp4')
    
    def stream_external_video_adv(self, request):
        url = self.link

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

        resp = requests.get(url, headers=headers, stream=True)

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
    
    def json(self):
      return {
        "id": self.id,
        "title": self.title,
        "path": self.path,
        "type": self.type,
        "link": self.link,
        "source": self.source,
        "stream": f"http://10.0.2.2:8000/stream/{self.id}",
      }