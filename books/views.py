from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from .models import Book, Quote
from .utils import search_books
from .forms import SignUpForm, LoginForm

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response

class LandingView(TemplateView):
    template_name = 'landing.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('bookshelf')
        return super().get(request, *args, **kwargs)

class BookshelfView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/shelf.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = Book.objects.filter(user=self.request.user)
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(author__icontains=q) |
                Q(notes__icontains=q)
            ).distinct()
        return queryset.order_by('-updated_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quote'] = Quote.objects.random()
        return context

class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'books/detail.html'
    context_object_name = 'book'

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quote'] = Quote.objects.random()
        return context

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    template_name = 'books/book_form.html'
    fields = ['title', 'author', 'cover_url', 'total_pages', 'status', 'notes']

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'"{form.instance.title}" has been added to your shelf.')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quote'] = Quote.objects.random()
        
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            try:
                search_results = search_books(search_query)
                context['search_query'] = search_query
                context['search_results'] = search_results
                if not search_results:
                    messages.info(self.request, 'No books found matching your search.')
            except Exception as e:
                messages.error(self.request, 'Unable to search for books at the moment.')
                print(f"Search error: {str(e)}")
        
        return context

    def post(self, request, *args, **kwargs):
        if 'select_book' in request.POST:
            try:
                book = Book.objects.create(
                    user=request.user,
                    title=request.POST.get('title', ''),
                    author=request.POST.get('author', ''),
                    cover_url=request.POST.get('cover_url', ''),
                    isbn13=request.POST.get('isbn13'),
                    status='plan_to_read'
                )
                messages.success(request, f'"{book.title}" has been added to your shelf.')
                return redirect('book_detail', pk=book.pk)
            except Exception as e:
                messages.error(request, 'An error occurred while adding the book.')
                print(f"Error adding book: {str(e)}")
                return redirect('book_create')
            
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.object.pk})

@login_required
def update_progress(request, pk):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=pk, user=request.user)
        current_page = int(request.POST.get('current_page', 0))
        
        if current_page > 0 and book.status == 'plan_to_read':
            book.status = 'reading'
            book.started_at = timezone.now()
        
        book.current_page = current_page
        if current_page >= book.total_pages:
            book.status = 'completed'
        
        book.save()
        return redirect('book_detail', pk=pk)

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = 'books/book_form.html'
    fields = ['title', 'author', 'cover_url', 'total_pages', 'status', 'notes']
    context_object_name = 'book'

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quote'] = Quote.objects.random()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Book updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.object.pk})

class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('bookshelf')
    
    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quote'] = Quote.objects.random()
        return context
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Book deleted successfully!')
        return super().delete(request, *args, **kwargs)
