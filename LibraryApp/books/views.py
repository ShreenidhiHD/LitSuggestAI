from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Book
from django.contrib import messages
from .gpt_service import generate_book_suggestion
import logging
import json


logging.basicConfig(level=logging.INFO)

def index_view(request):
    return render(request, 'index.html')

def view_books(request):
    if request.method == "POST":
      
        book_id = request.POST.get('book_id')
        Book.objects.filter(id=book_id).delete()
        return JsonResponse({"message": "Book deleted successfully."})
        
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})



def add_book_view(request):
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        cover_image = request.POST.get('cover_image')
        Book.objects.create(title=title, author=author, isbn=isbn, cover_image=cover_image)
        
        messages.success(request, 'Book added successfully.')
        return redirect('book_routes:add_book_view')
        
    return render(request, 'add_books.html')


def delete_book(request, book_id):  
    if request.method == "POST":
        Book.objects.filter(id=book_id).delete()
        return redirect('book_routes:view_books')

def suggest_book_view(request):
    if request.method == "POST":
        received_json_data = json.loads(request.body.decode("utf-8"))
        query = received_json_data.get('query')
        print(f"Received query: {query}")  
        suggestion = generate_book_suggestion(query)
        print(f"Suggestion generated: {suggestion}") 
        return JsonResponse({"suggestion": suggestion})