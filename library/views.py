from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from datetime import date, timedelta
from .models import Book, Borrowing
from .forms import BookForm, BorrowingForm


# 1. نمایش لیست کتاب‌ها (برای همه کاربران)
class BookListView(ListView):
    model = Book
    template_name = 'library/book_list.html'
    context_object_name = 'books'
    ordering = ['-id']

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            # ۱. پیدا کردن کدهای انگلیسی موضوع (مثلاً sci) که معادل فارسیشون با عبارت جستجو یکی هست
            matching_genres = []
            for code, label in Book.GENRE_CHOICES:
                if query in label:
                    matching_genres.append(code)

            # ۲. جستجو در عنوان، نام و نام خانوادگی نویسنده، و کدهای موضوعی که پیدا کردیم
            return Book.objects.filter(
                Q(title__icontains=query) |
                Q(author__first_name__icontains=query) |
                Q(author__last_name__icontains=query) |
                Q(genre__in=matching_genres)  # جستجو بر اساس موضوع فارسی
            ).distinct()

        return Book.objects.all()


# 2. نمایش جزئیات یک کتاب خاص
class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'
    context_object_name = 'book'


# 3. ثبت کتاب جدید (فقط برای کتابدار)
class BookCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book_form.html'
    success_url = reverse_lazy('book_list')

    def test_func(self):
        return self.request.user.role == 'librarian'


# 4. ثبت امانت جدید (فقط برای کتابدار)
class BorrowingCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Borrowing
    form_class = BorrowingForm
    template_name = 'library/borrowing_form.html'
    success_url = reverse_lazy('book_list')

    def test_func(self):
        return self.request.user.role == 'librarian'


# 5. درخواست امانت کتاب (برای اعضای کتابخانه)
def request_borrow(request, book_id):
    if not request.user.is_authenticated:
        return redirect('login')

    book = get_object_or_404(Book, pk=book_id)

    if book.available_copies > 0:
        # ساخت رکورد امانت (موعد بازگشت ۱۴ روز بعد)
        Borrowing.objects.create(
            member=request.user,
            book=book,
            due_date=date.today() + timedelta(days=14)
        )
        # کم کردن موجودی
        book.available_copies -= 1
        book.save()
        messages.success(request, f"کتاب «{book.title}» با موفقیت امانت گرفته شد.")
    else:
        messages.error(request, "این کتاب در حال حاضر موجود نیست.")

    return redirect('book_list')


# 6. مشاهده کتاب‌های امانت گرفته شده توسط کاربر
class MyBorrowingsView(LoginRequiredMixin, ListView):
    model = Borrowing
    template_name = 'library/my_borrowings.html'
    context_object_name = 'borrowings'

    def get_queryset(self):
        # فقط امانت‌های کاربری که لاگین کرده رو نشون بده
        return Borrowing.objects.filter(member=self.request.user).order_by('-borrow_date')