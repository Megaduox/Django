from django.core.management.base import BaseCommand

from news.crawlers.thedrive_crawler import parse_urls, parse_one_page


class Command(BaseCommand):
    help = 'Run Thedrive.com crawler'

    def handle(self, *args, **options):
        print('Crawler in running...')
        # for url in parse_urls('https://www.thedrive.com/reviews'):
        #     print('Парсим урл:', url)
        #     print(parse_one_page(url))

        parse_one_page('https://www.thedrive.com/reviews/27482/best-tire-shine')