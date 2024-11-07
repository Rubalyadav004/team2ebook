# books/admin.py

from django.contrib import admin
from .models import Book, Review, Cart

# Customize the Book model display in the admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'created_at')  # Fields displayed in the list view
    search_fields = ('title', 'author')  # Add search functionality for title and author
    list_filter = ('created_at',)  # Filter options for created date
    readonly_fields = ('created_at',)  # Make created_at read-only

# Customize the Review model display in the admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')
    search_fields = ('user__username', 'book__title')  # Add search for username and book title
    list_filter = ('rating', 'created_at')  # Filter options for rating and date

# Customize the Cart model display in the admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'added_at')
    search_fields = ('user__username', 'book__title')  # Search for user and book title
    list_filter = ('added_at',)  # Filter by date added
    readonly_fields = ('added_at',)  # Make added_at read-only
