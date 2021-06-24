from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.contrib import messages

from django.views.generic import TemplateView, ListView

from news.models import Article, Category, Comment
from news.forms import CommentsForm


class ContactView(TemplateView):
    template_name = "news/contacts.html"


class IndexView(TemplateView):
    template_name = "news/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_10_articles'] = Article.objects.all().order_by('-pub_date')[:10].prefetch_related('categories')
        return context


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


class BlogView(ListView):
    template_name = "news/blog.html"
    model = Article
    ordering = "-pub_date"
    paginate_by = 5

    def get_queryset(self):
        self.cat_slug = self.kwargs.get('cat_slug')
        qs = super().get_queryset()
        if self.cat_slug:
            qs = qs.filter(categories__slug=self.cat_slug)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.cat_slug:
            context['category'] = Category.objects.get(slug=self.cat_slug)
        return context


class RobotsView(TemplateView):
    template_name = "news/robots.txt"
    content_type = "text/plain"
