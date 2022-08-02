from django.urls import path

from . import views
import encyclopedia

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.get_Entry, name="title"),
    path("wiki/<str:querry>", views.search, name="search_Found"),
    path("wiki/search/", views.search, name="search_Not_Found"),
]

