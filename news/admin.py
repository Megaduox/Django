from django.contrib import admin

from .models import Category, Author, Article, Comment, Newsletter, Tag
from django_summernote.admin import SummernoteModelAdmin


class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content', 'short_description')


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Newsletter)
admin.site.register(Tag)
