from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import MenuItem, Table, Reservation
from jalali_date import date2jalali
import jdatetime


# -------------------- Portfolio Pages --------------------

def home(request):
    """Main portfolio landing page."""
    return render(request, "home.html")


def about(request):
    """About me page."""
    return render(request, "about.html")


def resume(request):
    """Resume / CV page."""
    return render(request, "resume.html")


def contact(request):
    """Contact form page."""
    return render(request, "contact.html")



def menu(request):
    """Static menu page — items manually written in menu.html"""
    return render(request, "menu.html")


def admin_guide(request):
    return render(request, "admin_guide.html")



# -------------------- Dynamic Menu Page --------------------

def dynamic_menu_view(request):
    appetizers = MenuItem.objects.filter(category="appetizer")
    mains = MenuItem.objects.filter(category="main")
    drinks = MenuItem.objects.filter(category="drink")

    context = {
        "appetizers": appetizers,
        "mains": mains,
        "drinks": drinks,
    }
    return render(request, "dynamic_menu.html", context)



# -------------------- Reservation Page --------------------

def reservation(request):
    """Restaurant reservation page."""
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        num_guests = int(request.POST.get("num_guests", 0))
        date_str = request.POST.get("date")
        time = request.POST.get("time")
        special_request = request.POST.get("special_request", "")

        # --- Step 1: Convert Jalali (Shamsi) to Gregorian safely ---
        try:
            parts = [int(x) for x in date_str.replace('-', '/').split('/')]
            j_date = jdatetime.date(parts[0], parts[1], parts[2])
            date = j_date.togregorian()
        except Exception:
            messages.error(request, "تاریخ وارد شده معتبر نیست. لطفاً دوباره امتحان کنید.")
            return redirect("reservation")

        # --- Step 2: Find available table ---
        possible_tables = Table.objects.filter(capacity__gte=num_guests).order_by("capacity")
        available_table = None

        for table in possible_tables:
            conflict_exists = Reservation.objects.filter(
                table=table,
                date=date,
                time=time,
                approved=True
            ).exists()
            if not conflict_exists:
                available_table = table
                break

        # --- Step 3: Create reservation record ---
        Reservation.objects.create(
            name=name,
            phone=phone,
            num_guests=num_guests,
            date=date,
            time=time,
            special_request=special_request,
            table=available_table,
        )

        # --- Step 4: Feedback message ---
        if available_table:
            jalali_date_str = date2jalali(date).strftime("%Y/%m/%d")
            messages.success(
                request,
                f"✅ رزرو شما ثبت شد! میز شماره {available_table.table_number} برای تاریخ {jalali_date_str} رزرو شد."
            )
        else:
            messages.warning(
                request,
                "❌ در حال حاضر میزی برای این تاریخ و ساعت موجود نیست. لطفاً با مدیر تماس بگیرید."
            )

        return redirect("reservation")

    return render(request, "reservation.html")
