from django.http import (
    HttpResponse,
    HttpResponseNotFound,
    Http404,
    HttpResponsePermanentRedirect, HttpResponseRedirect,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from packaging.tags import Tag

from human.froms import PostForm
from human.models import Human, Category, TagPost, Menu

def index(request):
    data = {
        "title": "Главная страница",
        "posts": Human.published.all().select_related('cat'),
        "cat_selected": 0,
    }
    return render(request, "human/index.html", context=data)

def menu_view(request, url_name):
    menu_item = get_object_or_404(Menu, url_name=url_name)  # Получаем конкретный пункт меню или возвращаем 404
    context = {'menu_item': menu_item}  # Передаем пункт меню в шаблон
    return render(request, 'human/menu.html', context) # Или другой шаблон

def show_post(request, post_slug):
    post = get_object_or_404(Human, slug=post_slug)
    data = {"title": post.title, "post": post, "cat_selected": 1}
    return render(request, "human/post.html", data)


def about(request):
    return render(request, "human/about.html", {"title": "О сайте"})


def addpage(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            try:
                Human.objects.create(**form.cleaned_data)
                return redirect("home")
            except:
                form.add_error(None, "Ошибка ввода данных.")

    else:
        form = PostForm()

    data ={
        'title': "Добавить СГ",
        'form': form,
    }
    return render(request, "human/addpage.html", data)


def login(request):
    return HttpResponse("Авторизация")


def contact(request):
    return HttpResponse("Обратная свазь")


def category(request, cat_slug):
    all_category = get_object_or_404(Category, slug=cat_slug)
    posts = Human.published.filter(cat_id=all_category.pk).select_related('cat')

    data = {
        "title": f"Рубрика: {all_category.name}",
        "posts": posts,
        "cat_selected": all_category.pk,
    }
    return render(request, "human/index.html", context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Human.Status.PUBLISH).select_related('cat')
    data = {
        "title": f'Теги: {tag.tag}',
        "posts": posts,
        "cat_selected": None
    }
    return render(request, "human/index.html", context=data)
