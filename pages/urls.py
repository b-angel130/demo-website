from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("resume/", views.resume, name="resume"),
    path("contact/", views.contact, name="contact"),
    path("menu/", views.menu, name="menu"),  #  static menu.html
    path("dynamic-menu/", views.dynamic_menu_view, name="dynamic_menu"),  #  dynamic menu
    path("reservation/", views.reservation, name="reservation"),
    path("admin-guide/", views.admin_guide, name="admin_guide"),

]
