from django import template
from django.db.models import Count

import human.views as views
from human.models import Category, TagPost, Menu

register = template.Library()


@register.inclusion_tag("human/show_categories.html")
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0).order_by("pk")
    return {"cats": cats, "cat_selected": cat_selected}

@register.inclusion_tag('human/list_tags.html')
def show_all_tags():
    return {"tags": TagPost.objects.annotate(total=Count('tags')).filter(total__gt=0).order_by("pk")}

@register.inclusion_tag('human/menu.html')
def show_menu():
    return {"menu": Menu.objects.all()}