from django.contrib import admin
from django.utils.html import format_html
from threading import Thread

from news.crawlers.thedrive_crawler import main

from .models import Category, Author, Article, Comment, Newsletter, Tag
from django_summernote.admin import SummernoteModelAdmin


def count_words(modeladmin, request, queryset):
    for object in queryset:
        text = object.content.replace('<p>', '').replace('</p>', '')
        words = text.split()
        object.content_words_count = len(words)
        object.save()


count_words.short_description = 'Make words count'


def get_fresh_news(modeladmin, request, queryset):
    for object in queryset:
        if object.name == 'Thedrive review team':
            Thread(target=main, args=()).start()


get_fresh_news.short_description = 'Get fresh news'


class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content', 'short_description')
    list_display = ('name', 'image_code', 'pub_date', 'slug', 'my_func', 'content_words_count', 'count_unique_words')
    list_filter = ('author', 'pub_date', 'categories')
    search_fields = ('name', 'author')
    actions = (count_words, )

    # не отображаются картинки, потому что в урл два раза /media/, не удалось исправить
    def image_code(self, object):
        return format_html('<img src="{}" style="max-width:50px">', object.main_image.url)

    def my_func(self, object):
        return 'My text field'


class AuthorArticleInline(admin.TabularInline):
    model = Article
    exclude = ('content', 'short_description')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'ava', )
    search_fields = ('name', )
    inlines = (AuthorArticleInline, )
    actions = (get_fresh_news, )

    # тут тоже не работают картинки, т.к. в пути media 2 раза, я пробовал переопределять - не удалось починить
    def ava(self, object):
        if object.avatar.url:
            return format_html('<img src="{}" style="max-width:30px">', object.avatar.url)
        else:
            return None


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'in_menu', 'order')
    list_filter = ('in_menu', )
    search_fields = ('name', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Newsletter)
admin.site.register(Tag)
