from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('book/add/', views.BookCreateView.as_view(), name='book_add'),
    path('borrow/add/', views.BorrowingCreateView.as_view(), name='borrow_add'),
    path('borrow/request/<int:book_id>/', views.request_borrow, name='request_borrow'),
    path('my-borrowings/', views.MyBorrowingsView.as_view(), name='my_borrowings'),
   
]