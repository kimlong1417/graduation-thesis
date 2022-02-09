from django.contrib import admin
from django.urls import path
from .views import login, register, test_view

urlpatterns = [
    path('login/', login, name="login"),
    path('register/', register, name="register"),
    path('', test_view, name="home")
]
