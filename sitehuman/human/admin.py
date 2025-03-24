from django.contrib import admin, messages
from django.template.defaultfilters import title

from .models import Human, Category

# Register your models here.

admin.site.site_header = "Мужики"
admin.site.index_title= "Столбцы"

class MarriedFilter(admin.SimpleListFilter):
    title = "Статус"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [
            ("married", "да"),
            ("single", "нет")
        ]

    def queryset(self, request, queryset):
        if self.value() == "married":
            return queryset.filter(husband__isnull=False)
        if self.value() == "single":
            return queryset.filter(husband__isnull=True)

@admin.register(Human)
class HumanAdmin(admin.ModelAdmin):
    fields =['title','slug' ,'cat', "is_published", "content"]
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title', 'time_create', "is_published",'cat', 'bref_info')
    list_display_links = ('id', 'title',)
    list_filter = ('is_published', "cat__name", MarriedFilter)
    list_per_page = 5
    list_editable = ('is_published',)
    actions = ['change_to_publish', 'change_to_unpublish', 'for_fun_day']
    search_fields = ["title", "cat__name"]


    @admin.display(description="Краткое описание")
    def bref_info(self, human: Human):
        return f"Количество символов {len(human.content)}"

    @admin.action(description="Опубликовать пост")
    def change_to_publish(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f"Опубликовано {count} записей")

    @admin.action(description="Снять с публикации")
    def change_to_unpublish(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request, f"Снято с публикации {count} записей", messages.WARNING)

    @admin.action(description='Изменить')
    def for_fun_day(self, request, queryset):
        is_pub = all(obj.is_published for obj in queryset)
        if is_pub:
            count = queryset.update(is_published=False)
            self.message_user(request, f"Снято с публикации {count} записей", messages.WARNING)
            return False
        else:
            count = queryset.update(is_published=True)
            self.message_user(request, f"Опубликовано {count} записей")
            return True



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    list_per_page = 5