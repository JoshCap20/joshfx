import os
import subprocess
from django.db import models
from django.http import StreamingHttpResponse
import requests

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
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


    def stream_video(self):
      print("Streaming video...")
      mp4_path = self.get_video()

      def generate():
          with open(mp4_path, 'rb') as f:
              for chunk in iter(lambda: f.read(4096), b""):
                  yield chunk

      os.remove(mp4_path)

      return StreamingHttpResponse(generate(), content_type='video/mp4')