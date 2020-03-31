from django.urls import path
from . import views

app_name = 'catalog_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.bookList, name='books'),
    path('check_out_book/', views.check_out_book, name='check_out_book')
]
