from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Banner
from .forms import CommentForm
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def index(request):
    banner = Banner.objects.all()[0]
    latest_posts = Post.objects.all().order_by("-date")[:6]
    most_viewed_posts = Post.objects.all().order_by("-view_count")[:6]
    return render(request, "blogs/index.html", { "banner": banner, "latest_posts": latest_posts, "most_viewed_posts": most_viewed_posts})

# class IndexView(ListView):
#     template_name = "blogs/index.html"
#     model = Post
#     ordering = ["-date"]
#     context_object_name = "posts"

#     def get_queryset(self):
#         query = super().get_queryset()
#         data = query[:6]
#         return data
    

def posts(request):
    all_posts = []
    if(request.method == "POST") :
        keyword = request.POST["keyword"]
        url = "posts?keyword={}".format(keyword)
        return HttpResponseRedirect(url)
    else:
        if "keyword" in request.GET:
            print("It does")
            keyword = request.GET["keyword"]
            all_posts = Post.objects.filter(title__icontains=keyword) | Post.objects.filter(view_count__icontains=keyword)  |  Post.objects.filter(content__icontains=keyword)
        else:
            print("It doesn't")
            all_posts = Post.objects.all().order_by("-date")
        return render(request, "blogs/all-posts.html", { "posts": all_posts })

# class PostsView(ListView):
#     template_name = "blogs/all-posts.html"
#     context_object_name = "posts"
#     model = Post
#     ordering = ["-date"]



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
        post.view_count = post.view_count + 1
        post.save()

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