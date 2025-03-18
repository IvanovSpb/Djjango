from django.db import models
from django.db.models import Q
from django.template.context_processors import request
from django.urls import reverse


# Create your models here.
class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Human.Status.PUBLISH)


class Human(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, "не опубликован"
        PUBLISH = 1, "Опубликован"

    title = models.CharField(max_length=255, verbose_name="Заголовки")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Адрес')
    content = models.TextField(blank=True, verbose_name="Контент")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name="Публикация")
    cat = models.ForeignKey("Category", on_delete=models.PROTECT, null=True, related_name="posts",
                            verbose_name="Категория")
    tags = models.ManyToManyField("TagPost", blank=True, related_name="tags", verbose_name="теги")
    husband = models.OneToOneField("Husband", on_delete=models.SET_NULL, null=True,
                                   blank=True, related_name="husband", verbose_name="Мужики")

    objects = models.Manager()
    published = PublishedModel()

    class Meta:
        verbose_name = "Мужики"
        verbose_name_plural = "Мужики"
        ordering = ["-time_create"]
        indexes = [
            models.Index(fields=["-time_create"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Предназначения")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Имя")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"cat_slug": self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class TagPost(models.Model):
    tag = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse("tag", kwargs={"tag_slug": self.slug})

class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)

    def __str__(self):
        return self.name
