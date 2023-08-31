from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib import admin

app_name = 'book_routes'

urlpatterns = [
    path('', views.index_view, name='home'), 
    path('books/', views.view_books, name='view_books'), 
    path('add_books/', views.add_book_view, name='add_book_view'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'), 
    path('suggest_book/', views.suggest_book_view, name='suggest_book'),
    path('admin/', admin.site.urls),
]
