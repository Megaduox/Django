from django.core.management.base import BaseCommand

from news.crawlers.thedrive_crawler import main


class Command(BaseCommand):
    help = 'Run Thedrive.com crawler'

    def handle(self, *args, **options):
        print('Crawler in running...')
        main()
