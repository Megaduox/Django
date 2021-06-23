from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.contrib import messages

from news.models import Article, Category, Comment
from news.forms import CommentsForm


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
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['article'] = main_article
            Comment.objects.create(**data)
            form = CommentsForm()
        else:
            messages.add_message(request, messages.INFO, 'Form not valid')
    else:
        form = CommentsForm()

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
               'prev_article': prev_article,
               'form': form
               }
    return render(request, 'news/single.html', context)


def blog_handler(request):
    current_page = int(request.GET.get('page', 1))
    articles_on_page = 5
    top_10_articles = Article.objects.all().order_by('-pub_date').prefetch_related('categories')
    paginator = Paginator(top_10_articles, articles_on_page)
    page_obj = paginator.get_page(current_page)
    context = {
        'top_10_articles': top_10_articles,
        'page_obj': page_obj,
        'paginator': paginator
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
