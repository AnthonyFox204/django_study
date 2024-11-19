from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Women, Category


class MarriedFilter(admin.SimpleListFilter):
    title = 'Marriage status'
    parameter_name = 'marriage-status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Married'),
            ('single', 'Single'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'content', 'post_photo', 'photo', 'cat', 'husband', 'tags')
    readonly_fields = ('post_photo',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat')
    list_display_links = ('title',)
    ordering = ('-time_create', 'title')
    list_editable = ('is_published',)
    list_per_page = 10
    actions = ('set_published', 'set_draft')
    search_fields = ('title', 'cat__name')
    list_filter = ('cat__name', 'is_published', MarriedFilter)
    save_on_top = True

    @admin.display(description='Image', ordering='content')
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f'<img src="{women.photo.url}" width="50">')
        return 'No Photo'

    @admin.action(description='Set Published')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f'{count} entries published.')

    @admin.action(description='Set Drafted')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f'{count} entries drafted.', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
