from django.test import TestCase, Client
from django.urls import reverse
from app.models import Movie


class TestViews(TestCase):
    @classmethod
    def setUpTestData(self):
        self.client = Client()
        self.movie1 = getTestMovie()

    def test_index_GET(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_GET_query(self):
        response = self.client.get(
            reverse('index'), {'q': self.movie1.title})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, self.movie1)

    def test_index_GET_type(self):
        response = self.client.get(
            reverse('index'), {'type': self.movie1.type})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, self.movie1)

    def test_stream_GET(self):
        response = self.client.get(
            reverse('stream', args=[self.movie1.id]))
        self.assertEqual(response.status_code, 200)

    def test_stream_GET_no_movie(self):
        response = self.client.get(
            reverse('stream', args=[999999]))
        self.assertEqual(response.status_code, 404)

    def test_stream_GET_no_query(self):
        try:
            response = self.client.get(
                reverse('stream'))
            raise Exception("Should have failed")
        except:
            pass

    def test_stream_GET_bad_query(self):
        response = self.client.get(
            reverse('stream', args=["bad_query"]))
        self.assertEqual(response.status_code, 404)

    def test_get_link_GET(self):
        response = self.client.get(
            reverse('get_link'), {'q': self.movie1.id})
        self.assertEqual(response.status_code, 302)

    def test_get_link_GET_no_movie(self):
        response = self.client.get(
            reverse('get_link'), {'q': 999999})
        self.assertEqual(response.status_code, 404)

    def test_get_link_GET_no_query(self):
        response = self.client.get(
            reverse('get_link'))
        self.assertEqual(response.status_code, 404)

    def test_get_results_GET(self):
        response = self.client.get(
            reverse('get_results'), {'q': self.movie1.title})
        self.assertEqual(response.status_code, 200)

    def test_get_results_GET_no_movie(self):
        response = self.client.get(
            reverse('get_results'), {'q': 999999})
        self.assertEqual(response.status_code, 404)

    def test_get_results_GET_no_query(self):
        response = self.client.get(
            reverse('get_results'))
        self.assertEqual(response.status_code, 404)


def getTestMovie():
    return Movie.objects.create(
        title="Family Guy, S10E01",
        path="/TV/Family%20Guy/Season%2010/Family%20Guy%20S10E01%20Lottery%20Fever.mkv",
        link="http://96.233.113.244/TV/Family%20Guy/Season%2010/Family%20Guy%20S10E01%20Lottery%20Fever.mkv",
        type="mkv",
        source="13",
    )
