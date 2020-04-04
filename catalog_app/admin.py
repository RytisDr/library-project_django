from django.contrib import admin
from .models import Author, Genre, Book, Magazine
# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Magazine)
