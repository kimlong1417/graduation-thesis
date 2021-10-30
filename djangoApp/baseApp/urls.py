from django.urls import path
from baseApp.views import home, register

urlpatterns = [
    path('home/', home, name="home"),
    path('register/', register, name="register"),
]
