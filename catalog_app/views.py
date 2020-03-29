from django.shortcuts import render
from catalog_app.models import Book, Author, BookInstance, Genre
from django.views import generic
# Create your views here.


def index(request):

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def BookList(request):
    books = Book.objects.all()
    context = {
        'book_list': books
    }
    return render(request, 'book_list.html', context)
