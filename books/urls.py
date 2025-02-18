from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    LandingView, BookshelfView, BookDetailView, 
    BookCreateView, BookUpdateView, BookDeleteView,
    update_progress, CustomLoginView, SignUpView
)

urlpatterns = [
    # Authentication
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='landing'), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    
    # Main views
    path('', LandingView.as_view(), name='landing'),
    path('shelf/', BookshelfView.as_view(), name='bookshelf'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('book/<int:pk>/progress/', update_progress, name='update_progress'),
    path('add/', BookCreateView.as_view(), name='book_create'),
    path('book/<int:pk>/edit/', BookUpdateView.as_view(), name='edit_book'),
    path('book/<int:pk>/delete/', BookDeleteView.as_view(), name='delete_book'),
]
