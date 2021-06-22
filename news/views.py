from django.shortcuts import render
from news.models import Article, Category
from django.core.exceptions import ObjectDoesNotExist


def contacts_handler(request):
    context = {}
    return render(request, 'news/contacts.html', context)


def index_handler(request):
    top_10_articles = Article.objects.all().order_by('-pub_date')[:10].prefetch_related('categories')
    context = {
        'top_10_articles': top_10_articles,
    }

    return render(request, 'news/index.html', context)


def single_handler(request, post_slug):
    main_article = Article.objects.get(slug=post_slug)
    try:
        prev_article = Article.objects.get(id=main_article.id-1)
    except ObjectDoesNotExist:
        prev_article = None
    try:
        next_article = Article.objects.get(id=main_article.id+1)
    except ObjectDoesNotExist:
        next_article = None
    article = Article.objects.get(slug=post_slug)
    context = {'article': article,
               'next_article': next_article,
               'prev_article': prev_article
               }
    return render(request, 'news/single.html', context)


def blog_handler(request):
    top_10_articles = Article.objects.all().order_by('-pub_date')[:10].prefetch_related('categories')
    context = {
        'top_10_articles': top_10_articles,
    }
    return render(request, 'news/blog.html', context)


def cat_handler(request, cat_slug):
    category = Category.objects.get(slug=cat_slug)
    top_10_articles = Article.objects.filter(
        categories__slug=cat_slug).order_by('-pub_date')[:10].prefetch_related('categories')
    context = {
        'top_10_articles': top_10_articles,
        'category': category,
    }
    return render(request, 'news/blog.html', context)


def robots_handler(request):
    context = {}
    return render(request, 'news/robots.txt', context, content_type='text/plain')
