import logging
from django.shortcuts import (
    render, get_object_or_404,
    redirect,
)
from django.utils import timezone
from blog.models import Post
from blog.forms import CommentForm
# caching imports:
# ------------------------
# from django.views.decorators.cache import cache_page
# from django.views.decorators.vary import vary_on_headers, vary_on_cookie


logger = logging.getLogger(__name__)

'''Without vary_on_headers the index view will cause a big problem
     because the logged in users and an anounymouseUser can share
     same response.
     Using vary_on_cookie is more convenient'''

# caching code
# ----------------------
# @cache_page(300)
# # @vary_on_headers('Cookie')
# @vary_on_cookie
# def index(request):
#     from django.http import HttpResponse
#     logger.debug("Index function is called!")
#     return HttpResponse(str(request.user).encode("ascii"))
#     posts = Post.objects.filter(published_at__lte=timezone.now())
#     logger.debug("Got %d posts", len(posts))
#     return render(request, "blog/index.html", {"posts": posts})

def get_ip(request):
  from django.http import HttpResponse
  return HttpResponse(request.META['REMOTE_ADDR'])
  
def index(request):
    # posts = Post.objects.filter(published_at__lte=timezone.now())
    # Optimization 1
    # posts = Post.objects.filter(published_at__lte=timezone.now()).select_related('author')
    # Optimization 2
    # posts = (
    #     Post.objects.filter(published_at__lte=timezone.now())
    #     .select_related("author")
    #     .defer("created_at", "modified_at")
    # )
    # Optimization 3
    posts = (
        Post.objects.filter(published_at__lte=timezone.now())
        .select_related("author")
        .only("title", "summary", "content", "author", "published_at", "slug")
    )
    logger.debug("Got %d posts", len(posts))
    return render(request, "blog/index.html", {"posts": posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_active:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                logger.info("Created comment on Post %d for user %s", post.pk, request.user)
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
    return render(
        request, "blog/post-detail.html", {"post": post, "comment_form": comment_form}
    )
