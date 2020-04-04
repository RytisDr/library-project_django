from django.shortcuts import render, get_object_or_404
from .models import Magazine, Book, Author, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import datetime, timedelta, date


@login_required
def index(request):

    num_books = Book.objects.all().count()
    num_authors = Author.objects.count()
    num_magazines = Magazine.objects.all().count()
    context = {
        'num_books': num_books,
        'num_authors': num_authors,
        'num_magazines': num_magazines,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


@login_required
def book_list(request):
    books = Book.objects.filter(status="a")
    context = {
        'book_list': books,
    }
    return render(request, 'book_list.html', context)


@login_required
def magazine_list(request):
    magazines = Magazine.objects.filter(status="a")
    context = {
        'magazine_list': magazines,
    }
    return render(request, 'magazine_list.html', context)


@login_required
def check_out_book(request):
    if not request.POST:
        return HttpResponseRedirect(reverse('catalog_app:books'))
    user = request.user
    user_magazines = Book.objects.filter(loaned_to=user)
    # check if any books past due date
    for book in user_magazines:
        due_back = book.due_back
        if due_back < date.today():
            return HttpResponse('<h1>You have some books past due date, return them first.</h1>')
    # limit check-out to 10 books
    borrowed_books_amount = user_magazines.count()
    if borrowed_books_amount < 10:
        pk = request.POST['id']
        book = get_object_or_404(Book, pk=pk)
        book.status = 'o'
        book.loaned_to = user
        book.due_back = datetime.now()+timedelta(days=30)
        book.save()
        return HttpResponseRedirect(reverse('catalog_app:books'))
    else:
        return HttpResponse('<h1>Cant have more than 10 books at the same time.</h1>')


@login_required
def check_out_magazine(request):
    if not request.POST:
        return HttpResponseRedirect(reverse('catalog_app:magazines'))
    user = request.user
    user_magazines = Magazine.objects.filter(loaned_to=user)
    # check if any magazines past due date
    for magazine in user_magazines:
        due_back = magazine.due_back
        if due_back < date.today():
            return HttpResponse('<h1>You have some magazines past due date, return them first.</h1>')
    # limit check-out to 3 magazines
    borrowed_magazines_amount = user_magazines.count()
    if borrowed_magazines_amount < 3:
        pk = request.POST['id']
        magazine = get_object_or_404(Magazine, pk=pk)
        magazine.status = 'o'
        magazine.loaned_to = user
        magazine.due_back = datetime.now()+timedelta(days=30)
        magazine.save()
        return HttpResponseRedirect(reverse('catalog_app:magazines'))
    else:
        return HttpResponse('<h1>Cant have more than 3 magazines at the same time.</h1>')
