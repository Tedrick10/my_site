from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import CommentForm
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

# def index(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blogs/index.html", { "posts": latest_posts })

class IndexView(ListView):
    template_name = "blogs/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        query = super().get_queryset()
        data = query[:3]
        return data
    

# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     return render(request, "blogs/all-posts.html", { "posts": all_posts })

class PostsView(ListView):
    template_name = "blogs/all-posts.html"
    context_object_name = "posts"
    model = Post
    ordering = ["-date"]


# def post_details(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)
#     return render(request, "blogs/post-details.html", { "post": identified_post, "post_tags": identified_post.tags.all() })

class PostDetailsView(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        
        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm,
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id),
        }
        return render(request, "blogs/post-details.html", context)

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(reverse("post_details", args=[slug]))
        
        
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm,
            "saved_for_later": self.is_stored_post(request, post.id),
        }

        return render(request, "blogs/post-details.html", context)
    
class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
        return render(request, "blogs/stored-posts.html", context)


    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts
        
        return HttpResponseRedirect("/")