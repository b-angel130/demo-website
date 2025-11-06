from django.db import models
from django.utils import timezone


# Create your models here.


# Menu item for the restaurant demo
class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('appetizer', 'پیش‌غذا / Appetizer'),
        ('main', 'غذای اصلی / Main'),
        ('drink', 'نوشیدنی / Drink'),
    ]

    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"





class Table(models.Model):
    table_number = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"Table {self.table_number} ({self.capacity} نفر)"


class Reservation(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    num_guests = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()
    special_request = models.TextField(blank=True, null=True)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.date} {self.time} ({self.num_guests} نفر)"