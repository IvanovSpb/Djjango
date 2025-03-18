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

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)
    cat = models.ForeignKey("Category", on_delete=models.PROTECT, null=True)
    tags = models.ManyToManyField("TagPost", blank=True, related_name="tags")
    husband = models.OneToOneField("Husband", on_delete=models.SET_NULL, null=True,
                                   blank=True, related_name="husband")

    objects = models.Manager()
    published = PublishedModel()

    class Meta:
        ordering = ["-time_create"]
        indexes = [
            models.Index(fields=["-time_create"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"cat_slug": self.slug})

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
