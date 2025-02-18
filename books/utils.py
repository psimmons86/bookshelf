import os
import time
import requests
from urllib.parse import quote
from datetime import datetime, timedelta

def search_books(query):
    """
    Search for books using the Google Books API.
    Returns a list of book dictionaries or empty list if the request fails.
    """
    api_url = 'https://www.googleapis.com/books/v1/volumes'
    
    try:
        params = {
            'q': f'intitle:{query}',  # Search in title for more relevant results
            'maxResults': '5',
            'orderBy': 'relevance',
            'printType': 'books'
        }
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        books = []
        for item in data.get('items', []):
            volume_info = item.get('volumeInfo', {})
            image_links = volume_info.get('imageLinks', {})
            
            cover_url = image_links.get('thumbnail', '')
            if cover_url:
                cover_url = cover_url.replace('http://', 'https://')
            
            books.append({
                'title': volume_info.get('title', ''),
                'author': ', '.join(volume_info.get('authors', [])),
                'cover_url': cover_url,
                'isbn13': next((id.get('identifier') for id in volume_info.get('industryIdentifiers', []) 
                              if id.get('type') == 'ISBN_13'), None),
            })
        return books
            
    except Exception as e:
        print(f"Error searching books: {str(e)}")
        return []

def fetch_book_quotes(max_results=5):
    """
    Fetch quotes from Google Books API by searching for books and extracting preview text.
    Returns a list of dictionaries containing quote information.
    """
    search_terms = ['literary quotes', 'famous passages', 'classic literature']
    quotes = []
    api_url = 'https://www.googleapis.com/books/v1/volumes'
    
    for term in search_terms:
        try:
            params = {
                'q': term,
                'maxResults': str(max_results),
                'printType': 'books',
                'orderBy': 'relevance'
            }
            
            response = requests.get(api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            for item in data.get('items', []):
                volume_info = item.get('volumeInfo', {})
                description = volume_info.get('description', '')
                
                if description:
                    import re
                    potential_quotes = re.findall(r'"([^"]+)"', description)
                    
                    for quote_text in potential_quotes:
                        if 20 <= len(quote_text) <= 300:
                            quotes.append({
                                'text': quote_text,
                                'author': ', '.join(volume_info.get('authors', ['Unknown'])),
                                'book_title': volume_info.get('title'),
                                'book_id': item.get('id')
                            })
            
        except Exception as e:
            print(f"Error fetching quotes for term '{term}': {str(e)}")
            continue
    
    return quotes

def get_random_quote():
    """
    Get a random quote from the database, or fetch new ones if none exist.
    Returns a Quote object or None if no quotes are available.
    """
    from .models import Quote
    
    quote = Quote.objects.random()
    if not quote:
        # If no quotes in database, fetch some from Google Books
        quotes_data = fetch_book_quotes()
        for quote_data in quotes_data:
            Quote.objects.create(**quote_data)
        quote = Quote.objects.random()
    
    return quote
