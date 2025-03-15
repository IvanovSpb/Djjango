from django.http import (
    HttpResponse,
    HttpResponseNotFound,
    Http404,
    HttpResponsePermanentRedirect,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from packaging.tags import Tag

from human.models import Human, Category, TagPost

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "addpage"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]

data_db = [
    {
        "id": 1,
        "title": "Анджелина Джоли",
        "content": "Биография Анджелины Джоли",
        "is_published": True,
    },
    {
        "id": 2,
        "title": "Марго Робби",
        "content": "Биография Марго Робби",
        "is_published": False,
    },
    {
        "id": 3,
        "title": "Джулия Робертс",
        "content": "Биография Джулии Робертс",
        "is_published": True,
    },
]


def index(request):
    data = {
        "title": "Главная страница",
        "menu": menu,
        "posts": Human.published.all(),
        "cat_selected": 0,
    }
    return render(request, "human/index.html", context=data)


def show_post(request, post_slug):
    post = get_object_or_404(Human, slug=post_slug)

    data = {"title": post.title, "menu": menu, "post": post, "cat_selected": 1}
    return render(request, "human/post.html", data)


def about(request):
    return render(request, "human/about.html", {"title": "О сайте", "menu": menu})


def addpage(request):
    return HttpResponse("Добавление статьи")


def login(request):
    return HttpResponse("Авторизация")


def contact(request):
    return HttpResponse("Обратная свазь")


def category(request, cat_slug):
    all_category = get_object_or_404(Category, slug=cat_slug)
    posts = Human.published.filter(cat_id=all_category.pk)

    data = {
        "title": f"Рубрика: {all_category.name}",
        "menu": menu,
        "posts": posts,
        "cat_selected": all_category.pk,
    }
    return render(request, "human/index.html", context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Human.Status.PUBLISH)
    data = {
        "title": f'Теги: {tag.tag}',
        "menu": menu,
        "posts": posts,
        "cat_selected": None
    }
    return render(request, "human/index.html", context=data)
