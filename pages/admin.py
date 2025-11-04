from django.contrib import admin
from .models import MenuItem, Table, Reservation
from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date import datetime2jalali
from datetime import datetime


# -------------------- Menu Items --------------------
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "created_at")
    list_filter = ("category",)
    search_fields = ("name", "description")


# -------------------- Tables --------------------
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("table_number", "capacity")
    search_fields = ("table_number",)


# -------------------- Reservations --------------------
@admin.register(Reservation)
class ReservationAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('name', 'table', 'get_jalali_date', 'time', 'num_guests', 'approved')

    def get_jalali_date(self, obj):
        date_value = obj.date
        if isinstance(date_value, datetime):
            dt = date_value
        else:
            from datetime import datetime as dt_class
            dt = dt_class.combine(date_value, dt_class.min.time())
        return datetime2jalali(dt).strftime('%Y/%m/%d')

    get_jalali_date.short_description = 'تاریخ (شمسی)'
