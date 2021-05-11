import requests
import os
import datetime

from slugify import slugify
from requests_html import HTMLSession

from bs4 import BeautifulSoup


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
    # domain = f'https://www.thedrive.com{url}'
    content = list()
    with HTMLSession() as session:
        response = session.get(url)
        check_for_redirect(response)
        response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    name = soup.find('h1', class_='title').text
    content_intro = soup.find('div', class_='review-intro')
    content.append(content_intro)
    content_table = soup.find('div', class_='articleFragment')
    content.append(content_table)
    short_description = soup.find('div', class_='review-intro').text
    pub_date = soup.find('div', class_='review-date').text.split('\xa0')[1].strip()
    datetime_obj = datetime.datetime.strptime(pub_date, '%b %d, %Y')
    author = 'Thedrive review team'
    categories = [
        {
            'name': 'reviews',
            'slug': 'reviews'
        }
    ]
    main_image = soup.find('div', class_='review-product-image').find('img')['src']
    image_name = slugify(name)
    image_type = main_image.split('.')[-1]
    image_path = os.path.join('media', 'images', f'{image_name}.{image_type}')
    with open(image_path, 'wb') as file:
        with HTMLSession() as session:
            response = session.get(main_image)
            file.write(response.content)
    slug = slugify(name)

    breakpoint()
    article = {
        'name': name,
        'content': content,
        'short_description': short_description,
        'pub_date': datetime_obj.date(),
        'author': author,
        'categories': categories,
        'main_image': image_path,
        'slug': slug
    }

    return article

'''
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    content = models.TextField()
    short_description = models.TextField()
    main_image = models.ImageField(upload_to='images')
    pub_date = models.DateField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
'''