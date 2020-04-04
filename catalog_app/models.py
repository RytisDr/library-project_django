from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date
from django import template

register = template.Library()


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character ISBN')
    genre = models.ManyToManyField(Genre, help_text='Select a genre')
    due_back = models.DateField(null=True, blank=True)
    loaned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def genre_names(self):
        return ', '.join([i.name for i in self.genre.all()])

    def days_left(self):
        today = date.today()
        days_left = self.due_back - today
        if(days_left.days == 1):
            return "1 day left"
        if(days_left.days == 0):
            return "Today"
        if(days_left.days < 0):
            return "Overdue!"
        return f'{days_left.days} days left'

    @register.simple_tag
    def get_class_name(self):
        return self.__class__.__name__

    def __str__(self):
        return f'{self.title}'


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    # def get_absolute_url(self):
    #    return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Magazine(models.Model):
    title = models.CharField(max_length=200)
    issue = models.DateField()
    summary = models.TextField(
        max_length=1000, help_text='Enter a brief description of the magazine')
    issn = models.CharField('ISSN', max_length=8,
                            help_text='8 Character ISSN')
    due_back = models.DateField(null=True, blank=True)
    loaned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def days_left(self):
        today = date.today()
        days_left = self.due_back - today
        if(days_left.days == 1):
            return "1 day left"
        if(days_left.days == 0):
            return "Today"
        if(days_left.days < 0):
            return "Overdue!"
        else:
            return f'{days_left.days} days left'

    @register.simple_tag
    def get_class_name(self):
        return self.__class__.__name__

    def __str__(self):
        return f'{self.title}'
