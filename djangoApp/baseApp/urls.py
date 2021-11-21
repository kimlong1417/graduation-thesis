from os import name
from django.urls import path
from baseApp.controllers.UserRegister import registerUser
from baseApp.controllers.UserLogin import loginUser
from baseApp.controllers.Base64 import home, base64

urlpatterns = [
    # path('account/', AccountAPIView.as_view(), name="home"),
    path('register/', registerUser, name="registerUser"),
    path('login/', loginUser, name="loginUser"),
    path('home/', home, name="home"),
    path('readbase64/', base64, name="readbase64")
]
