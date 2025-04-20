from django.shortcuts import render
from .models import Book

def books_view(request):
    template = 'books/books_main.html'
    context = {}
    return render(request, template, context)


def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/books_list.html', {'books': books})
    # template = 'books/books_list.html'
    # context = {}
    # return render(request, template, context)
