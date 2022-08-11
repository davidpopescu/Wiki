from django.urls import path

from . import views
import encyclopedia

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.get_Entry, name="title"),
    path("search/", views.search, name="search"),
    path("search/<str:entry_Title>", views.search, name="search_Entry"),
    path("create/", views.create_Page, name="create_Page"),
    path("edit/<str:entry>", views.edit_Page, name="edit_Page"),
    path("random/", views.random_Page, name="random_Page"),
]

