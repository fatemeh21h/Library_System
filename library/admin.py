from django.contrib import admin
from .models import Author, Book, Borrowing, Reservation

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Borrowing)
admin.site.register(Reservation)