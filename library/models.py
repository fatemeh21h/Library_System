from django.db import models
from django.conf import settings

class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="نام")
    last_name = models.CharField(max_length=100, verbose_name="نام خانوادگی")
    birth_year = models.IntegerField(null=True, blank=True, verbose_name="سال تولد")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    GENRE_CHOICES = [
        ('sci', 'علمی'),
        ('sfi', 'علمی تخیلی'),
        ('fan', 'فانتزی'),
        ('nov', 'رمان'),
        ('his', 'تاریخی'),
        ('psy', 'روانشناسی'),
        ('poe', 'شعر'),
        ('art', 'هنر'),
        ('rel', 'مذهبی'),
        ('bio', 'زندگی‌نامه'),
        ('chi', 'کودک و نوجوان'),
    ]
    title = models.CharField(max_length=200, verbose_name="عنوان")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="نویسنده")
    publish_year = models.IntegerField(verbose_name="سال انتشار")
    publisher = models.CharField(max_length=200, verbose_name="ناشر")
    genre = models.CharField(max_length=10, choices=GENRE_CHOICES, verbose_name="موضوع")
    total_copies = models.IntegerField(default=1, verbose_name="تعداد کل نسخه ها")
    available_copies = models.IntegerField(default=1, verbose_name="تعداد موجود")

    def __str__(self):
        return self.title

class Borrowing(models.Model):
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="عضو")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="کتاب")
    borrow_date = models.DateField(auto_now_add=True, verbose_name="تاریخ امانت")
    due_date = models.DateField(verbose_name="موعد بازگشت")
    return_date = models.DateField(null=True, blank=True, verbose_name="تاریخ بازگشت")
    is_returned = models.BooleanField(default=False, verbose_name="بازگشت داده شده")
    penalty = models.IntegerField(default=0, verbose_name="جریمه (تومان)")

    def __str__(self):
        return f"{self.book.title} -> {self.member.username}"

class Reservation(models.Model):
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="عضو")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="کتاب")
    reservation_date = models.DateField(auto_now_add=True, verbose_name="تاریخ رزرو")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    def __str__(self):
        return f"رزرو {self.book.title} توسط {self.member.username}"