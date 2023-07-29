from django.contrib import admin
from django.urls import path

from app.tv_apis import get_link, get_results
from app.website_views import IndexView, SearchAPI, js_stream, stream

urlpatterns = [
    path("admin/", admin.site.urls),

    ## Website Views
    path("", IndexView.as_view(), name="index"),
    path("search/", SearchAPI.as_view(), name="search"),

    ## Streams
    path("stream/<str:query>", stream, name="stream"), # Server Stream (returns HTTPStreamingResponse)
    path("streams/<str:query>", js_stream, name="js_stream"), # Client Stream (returns HTTP page)

    ## TV APIs
    path("api/", get_link, name="get_link"),
    path("results/", get_results, name="get_results"),
]
