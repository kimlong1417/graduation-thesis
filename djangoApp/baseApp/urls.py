from django.urls import path
from baseApp.controllers.UserRegister import registerUser
from baseApp.controllers.UserLogin import loginUser
from baseApp.controllers.Base64 import home

urlpatterns = [
    # path('account/', AccountAPIView.as_view(), name="home"),
    path('register/', registerUser, name="registerUser"),
    path('login/', loginUser, name="loginUser"),
    path('home/', home, name="home"),
]
