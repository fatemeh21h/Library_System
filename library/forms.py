from django import forms
from .models import Book, Borrowing

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title','author','publish_year','publisher','genre','total_copies','available_copies']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
            'publish_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_copies': forms.NumberInput(attrs={'class': 'form-control'}),
            'available_copies': forms.NumberInput(attrs={'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),


        }


class BorrowingForm(forms.ModelForm):
    class Meta:
        model = Borrowing
        fields = ['member', 'book', 'due_date']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-control'}),
            'book': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control' , 'type': 'date'}),
        }
