from django import template
import human.views as views
from human.models import Category, TagPost

register = template.Library()


@register.inclusion_tag("human/show_categories.html")
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {"cats": cats, "cat_selected": cat_selected}

@register.inclusion_tag('human/list_tags.html')
def show_all_tags():
    return {"tags": TagPost.objects.all()}