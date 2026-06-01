from django.contrib import admin
from .models import Category, Article, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'created_at',
        'updated_at',
        'is_published'
    )
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ("title",)}
    list_filter = ('is_published', 'category', 'created_at')
    list_editable = ('is_published',)
    date_hierarchy = 'created_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'article', 'created_at')
    search_fields = ('author_name', 'article__title')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
