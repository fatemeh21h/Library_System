from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('librarian', 'کتابدار'),
        ('member', 'عضو کتابخانه'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='member', verbose_name="نقش کاربر")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="شماره تماس")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"