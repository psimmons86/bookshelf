from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    STATUS_CHOICES = [
        ('reading', 'Reading'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('dropped', 'Dropped'),
        ('plan_to_read', 'Plan to Read'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    cover_url = models.URLField(blank=True, null=True)
    isbn13 = models.CharField(max_length=13, blank=True, null=True)
    total_pages = models.IntegerField(default=0)
    current_page = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='plan_to_read')
    notes = models.TextField(blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def progress(self):
        if self.total_pages == 0:
            return 0
        return int((self.current_page / self.total_pages) * 100)

class QuoteManager(models.Manager):
    def random(self):
        return self.order_by('?').first()

class Quote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=200)
    book_title = models.CharField(max_length=200, blank=True, null=True)
    book_id = models.CharField(max_length=50, blank=True, null=True)  # Google Books volume ID
    created_at = models.DateTimeField(auto_now_add=True)

    objects = QuoteManager()

    def __str__(self):
        source = self.book_title if self.book_title else "Unknown source"
        return f"{self.text[:50]}... - {self.author} ({source})"
