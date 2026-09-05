from django.core.paginator import Paginator
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, render

from .models import Category, Post


def post_list(request, slug=None):
    posts = Post.published.select_related("category")
    category = None

    if slug:
        category = get_object_or_404(Category, slug=slug)
        posts = posts.filter(category=category)

    query = request.GET.get("q", "").strip()
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(tags__icontains=query)
        )

    page_obj = Paginator(posts, 6).get_page(request.GET.get("page"))

    return render(
        request,
        "blog/post_list.html",
        {
            "page_obj": page_obj,
            "posts": page_obj.object_list,
            "categories": Category.objects.all(),
            "category": category,
            "query": query,
        },
    )


def post_detail(request, slug):
    post = get_object_or_404(Post.published.select_related("category"), slug=slug)
    Post.objects.filter(pk=post.pk).update(views=F("views") + 1)

    related = Post.published.filter(category=post.category).exclude(pk=post.pk)[:3]
    return render(request, "blog/post_detail.html", {"post": post, "related": related})
