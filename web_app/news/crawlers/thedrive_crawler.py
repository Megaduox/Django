import requests
import os
import datetime
import json

from django.db.utils import IntegrityError

from concurrent.futures import ThreadPoolExecutor

from slugify import slugify
from requests_html import HTMLSession
from bs4 import BeautifulSoup

from news.models import Article, Author, Category


def check_for_redirect(response_check):
    if response_check.history:
        raise requests.HTTPError
    else:
        pass


def parse_urls(root_url):
    links_urls = []
    response = requests.get(root_url)
    check_for_redirect(response)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    links = soup.find_all('a', class_='linkable')
    for link in links:
        links_urls.append(link.get('href'))
    return links_urls


def parse_one_page(url):
    domain = f'https://www.thedrive.com{url}'
    content = list()
    with HTMLSession() as session:
        response = session.get(domain)
        check_for_redirect(response)
        response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    name = soup.find('h1', class_='title').text
    print(name)
    content_intro = soup.find('div', class_='review-intro')
    content.append(content_intro)
    content_table = soup.find('div', class_='articleFragment')
    content.append(content_table)
    short_description = soup.find('div', class_='review-intro').text
    script = soup.find('script', type='application/ld+json')
    data = json.loads(soup.find('script', type='application/ld+json').next)
    pub_date = data[0]['datePublished'].split('T')[0]
    datetime_obj = datetime.datetime.strptime(pub_date, '%Y-%m-%d')
    author, is_author_created = Author.objects.get_or_create(
        name='Thedrive review team'
    )
    categories = [
        {
            'name': 'reviews',
            'slug': 'reviews'
        },
        {
            'name': 'best',
            'slug': 'best'
        }
    ]
    main_image = soup.find('div', class_='review-product-image').find('img')['src']
    image_name = slugify(name)
    image_type = main_image.split('.')[-1][:3]
    # image_path = os.path.join('media', 'images', f'{image_name}.{image_type}')
    # with open(image_path, 'wb') as file:
    #     with HTMLSession() as session:
    #         response = session.get(main_image)
    #         file.write(response.content)
    image_path = f'images/{image_name}.{image_type}'
    with open(f'media/{image_path}', 'wb') as f:
        with HTMLSession() as session:
            response = session.get(main_image)
        f.write(response.content)

    slug = slugify(name)
    article = {
        'name': name,
        'content': content,
        'short_description': short_description,
        'pub_date': datetime_obj,
        'author': author,
        'main_image': image_path,
        'slug': slug
    }

    # такой код работает
    try:
        article = Article(**article)
        article.save()
    except IntegrityError:
        article = Article.objects.get(slug=slug)
        print('Такая статья уже есть в базе')

    # По коду ниже ошибка "'NoneType' object is not callable"
    #
    # article, created = Article.objects.get_or_create(**article)
    #
    for category in categories:
        cat, created = Category.objects.get_or_create(**category)
        article.categories.add(cat)

    return article


def main():
    # for url in parse_urls('https://www.thedrive.com/reviews'):
    #     print('Парсим урл:', url)
    #     print(parse_one_page(url))
    # all_urls = parse_urls('https://www.thedrive.com/reviews')
    # with ThreadPoolExecutor(max_workers=10) as executor:
    #     executor.map(parse_one_page, all_urls)

    # Article.objects.all().delete()
    parse_one_page('/reviews/27479/best-obd2-scanner')
