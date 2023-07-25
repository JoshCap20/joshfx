from django.contrib import admin
from django.urls import path

from app.tv_apis import get_link, get_results
from app.website_views import IndexView, stream, SearchAPI

urlpatterns = [
    path("admin/", admin.site.urls),

    ## Website Views
    path("", IndexView.as_view(), name="index"),
    path("search/", SearchAPI.as_view(), name="search"),
    path("stream/<str:query>", stream, name="stream"),

    ## TV APIs
    path("api/", get_link, name="get_link"),
    path("results/", get_results, name="get_results"),
]
