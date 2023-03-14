from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("posts", views.posts, name="posts"),
    path("posts/<str:slug>", views.PostDetailsView.as_view(), name="post_details"),
    path("read-later", views.ReadLaterView.as_view(), name="read_later"),
]