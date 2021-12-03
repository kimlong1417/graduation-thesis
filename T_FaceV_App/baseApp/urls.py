"""Face_V URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from baseApp.controllers.CompareImage import compareImage
from baseApp.controllers.CompareImage2 import compareImage2
from baseApp.controllers.ObjectMatching import objectmatching
from baseApp.controllers.UserRegister import registerUser
from baseApp.controllers.UserLogin import loginUser
from baseApp.controllers.SplitAndDisplay import display3chanels
from baseApp.controllers.Home import Home, postBase64_process
urlpatterns = [
    # path('account/', AccountAPIView.as_view(), name="home"),
    path('register/', registerUser, name="registerUser"),
    path('login/', loginUser, name="loginUser"),
    path('home/', Home, name="Home"),
    path('display3chanels/', display3chanels, name="display3chanels"),
    path('objectmatching/', objectmatching, name="objectmatching"),
    path('compareimage/', compareImage, name="compareImage"),
    path('compareimage2/', compareImage2, name="compareImage2"),
    # path('home/', postBase64_process, name="postBase64_process"),
]