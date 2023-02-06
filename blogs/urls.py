from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("posts", views.PostsView.as_view(), name="posts"),
    path("posts/<slug:slug>", views.PostDetailsView.as_view(), name="post_details"),
    path("read-later", views.ReadLaterView.as_view(), name="read_later"),
]