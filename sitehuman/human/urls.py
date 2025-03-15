from django.urls import path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path("", views.index, name="home"),
    path("post/<slug:post_slug>", views.show_post, name="post"),
    path("about/", views.about, name="about"),
    path("addpage/", views.addpage, name="addpage"),
    path("login/", views.login, name="login"),
    path("contact/", views.contact, name="contact"),
    path("category/<slug:cat_slug>", views.category, name="category"),
    path("tag/<slug:tag_slug>", views.show_tag_postlist, name="tag"),
]
