from django import forms
from .models import *

class PostForm(forms.Form):
    title = forms.CharField(max_length=255, label="Название")
    slug = forms.SlugField(max_length=255, label="URL")
    content = forms.CharField(widget=forms.Textarea(attrs={"cols" :50, "rows":8}), label="Контент")
    is_published = forms.BooleanField(required=False, label="Опубликован")
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label="Категория")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), label="Мужик", required=False)