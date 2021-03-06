from django.urls import path
from . import views

app_name = 'catalog_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.book_list, name='books'),
    path('magazines/', views.magazine_list, name='magazines'),
    path('check_out_book/', views.check_out_book, name='check_out_book'),
    path('check_out_magazine/', views.check_out_magazine,
         name='check_out_magazine'),
    path('return/', views.return_article, name='return'),
    path('past_due/', views.past_due, name='past_due'),
    path('my_books/', views.my_books, name='my_books'),
]
