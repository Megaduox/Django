from django.shortcuts import render


def contacts_handler(request):
    context = {}
    return render(request, 'news/contacts.html', context)


def index_handler(request):
    context = {}
    return render(request, 'news/index.html', context)


def single_handler(request):
    context = {}
    return render(request, 'news/single.html', context)


def blog_handler(request):
    context = {}
    return render(request, 'news/blog.html', context)


def robots_handler(request):
    context = {}
    return render(request, 'news/robots.txt', context, content_type='text/plain')
