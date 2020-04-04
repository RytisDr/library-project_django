from django.shortcuts import render, get_object_or_404
from .models import Magazine, Book, Author, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import datetime, timedelta, date
import collections


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
def past_due(request):
    user = request.user
    if user.is_staff:
        context = collections.defaultdict(list)
        books_on_loan = Book.objects.filter(status="o")
        magazines_on_loan = Magazine.objects.filter(status="o")
        for magazine in magazines_on_loan:
            if magazine.due_back < date.today():
                context["late_magazines"].append(magazine)

        for book in books_on_loan:
            if book.due_back < date.today():
                context["late_books"].append(book)

        return render(request, 'past_due.html', context)
    else:
        return HttpResponseRedirect(reverse('catalog_app:index'))


@login_required
def my_books(request):
    user = request.user
    if not user.is_staff:
        context = collections.defaultdict(list)
        books_on_loan = Book.objects.filter(loaned_to=user)
        magazines_on_loan = Magazine.objects.filter(loaned_to=user)
        for magazine in magazines_on_loan:
            context["my_magazines"].append(magazine)
        for book in books_on_loan:
            context["my_books"].append(book)

        return render(request, 'my_books.html', context)
    else:
        return HttpResponseRedirect(reverse('catalog_app:index'))


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
        magazine.due_back = datetime.now()+timedelta(days=7)
        magazine.save()
        return HttpResponseRedirect(reverse('catalog_app:magazines'))
    else:
        return HttpResponse('<h1>Cant have more than 3 magazines at the same time.</h1>')


@login_required
def return_article(request):
    if not request.POST:
        return HttpResponseRedirect(reverse('catalog_app:my_books'))
    # turn string into variable name
    type_of_return = eval(request.POST['type'])
    article_pk = request.POST['pk']
    item_to_return = get_object_or_404(type_of_return, pk=article_pk)
    if(item_to_return):
        item_to_return.due_back = None
        item_to_return.loaned_to = None
        item_to_return.status = 'a'
        item_to_return.save()

    return HttpResponseRedirect(reverse('catalog_app:my_books'))
