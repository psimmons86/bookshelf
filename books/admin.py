from django.contrib import admin
from .models import Book, Quote

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'author')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'created_at')
    search_fields = ('text', 'author')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
