from django.urls import path
from baseApp.controllers.UserRegister import registerUser
from baseApp.controllers.UserLogin import loginUser

urlpatterns = [
    # path('account/', AccountAPIView.as_view(), name="home"),
    path('register/', registerUser, name="registerUser"),
    path('login/', loginUser, name="loginUser"),
]
