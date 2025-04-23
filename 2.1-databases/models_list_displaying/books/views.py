from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Book

def books_view(request):
    template = 'books/books_main.html'
    context = {}
    return render(request, template, context)

def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/books_list.html', {'books': books})

def book_detail_by_date(request, pub_date):
    date_object = datetime.strptime(pub_date, "%Y-%m-%d").date()
    book = Book.objects.filter(pub_date=date_object).first()
    if not book:
        return render(request, 'books/no_books_found.html')

    previous_date = Book.objects.filter(pub_date__lt=date_object).order_by('-pub_date').first()
    next_date = Book.objects.filter(pub_date__gt=date_object).order_by('pub_date').first()

    context = {
        'book': book,
        'previous_date': previous_date.pub_date.strftime("%Y-%m-%d") if previous_date else None,
        'next_date': next_date.pub_date.strftime("%Y-%m-%d") if next_date else None,
    }
    return render(request, 'books/book_detail.html', context)