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
    
    def get_video(self):
      print("Getting video...")
      response = requests.get(self.link, stream=True)

      # Assume the URL's last segment after the last slash is the file name
      file_name = self.link.split("/")[-1]
      file_ext = file_name.split(".")[-1]
      input_path = f'/tmp/input.{file_ext}'

      # If the file is already an mp4, we don't need to convert
      if file_ext.lower() == 'mp4':
          output_path = input_path
      else:
          output_path = '/tmp/output.mp4'

      with open(input_path, 'wb') as f:
          for chunk in response.iter_content(chunk_size=4096):
              f.write(chunk)

      # Convert the file if necessary
      if input_path != output_path:
          subprocess.run(['ffmpeg', '-i', input_path, output_path])
          os.remove(input_path)

      return output_path
    
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

    def stream_video(self):
      print("Streaming video...")
      mp4_path = self.get_video()

      def generate():
          with open(mp4_path, 'rb') as f:
              for chunk in iter(lambda: f.read(4096), b""):
                  yield chunk

      os.remove(mp4_path)

      return StreamingHttpResponse(generate(), content_type='video/mp4')
    
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