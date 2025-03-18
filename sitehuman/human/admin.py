from django.contrib import admin
from .models import Human, Category

# Register your models here.

admin.site.site_header = "Мужики"
admin.site.index_title= "Столбцы"

@admin.register(Human)
class HumanAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', "is_published",'cat')
    list_display_links = ('id', 'title',)
    list_filter = ('is_published',)
    list_per_page = 5

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    list_per_page = 5