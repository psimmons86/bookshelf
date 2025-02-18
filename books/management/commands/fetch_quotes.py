from django.core.management.base import BaseCommand
from books.utils import fetch_book_quotes
from books.models import Quote

class Command(BaseCommand):
    help = 'Fetch quotes from Google Books API and store them in the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--max-results',
            type=int,
            default=10,
            help='Maximum number of results per search term'
        )

    def handle(self, *args, **options):
        max_results = options['max_results']
        self.stdout.write('Fetching quotes from Google Books...')
        
        quotes_data = fetch_book_quotes(max_results=max_results)
        count = 0
        
        for quote_data in quotes_data:
            # Check if quote already exists to avoid duplicates
            if not Quote.objects.filter(
                text=quote_data['text'],
                author=quote_data['author']
            ).exists():
                Quote.objects.create(**quote_data)
                count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully added {count} new quotes to the database'
            )
        )
