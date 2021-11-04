from django.urls import path
from baseApp.views import registerUser, loginUser

urlpatterns = [
    # path('account/', AccountAPIView.as_view(), name="home"),
    path('register/', registerUser, name="registerUser"),
    path('login/', loginUser, name="loginUser"),
]
