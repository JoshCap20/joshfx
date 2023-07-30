from django.db import models

from app import streams


class Movie(models.Model):
    title = models.CharField(max_length=100)
    path = models.CharField(max_length=200)
    type = models.CharField(max_length=30)
    link = models.CharField(max_length=200)
    source = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def stream_external_video(self):
        # UNUSED
        return streams.stream_external_video(self)

    def stream_external_video_adv(self, request):
        return streams.stream_external_video_adv(self, request)

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "path": self.path,
            "type": self.type,
            "link": self.link,
            "source": self.source,
            "stream": f"http://127.0.0.1:8000/streams/{self.id}",
        }


class RequestManager(models.Manager):
    def get_or_create(self, info):
        try:
            request = self.get(info=info)
            request.count += 1
            request.save()
            return request
        except Request.DoesNotExist:
            return self.create(info=info)


class Request(models.Model):
    info = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=1)

    objects = models.Manager()

    def __str__(self):
        return self.info + " - " + str(self.date) + " - " + str(self.count)
