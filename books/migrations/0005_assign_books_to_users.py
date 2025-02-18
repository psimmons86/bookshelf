from django.db import migrations

def assign_books_to_first_user(apps, schema_editor):
    Book = apps.get_model('books', 'Book')
    User = apps.get_model('auth', 'User')
    
    # Get first user or create one if none exists
    user = User.objects.first()
    if not user:
        user = User.objects.create_user(username='admin', password='admin')
    
    # Assign all books without a user to this user
    Book.objects.filter(user__isnull=True).update(user=user)

def reverse_func(apps, schema_editor):
    Book = apps.get_model('books', 'Book')
    Book.objects.all().update(user=None)

class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_book_user'),
    ]

    operations = [
        migrations.RunPython(assign_books_to_first_user, reverse_func),
    ]
