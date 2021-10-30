from django.urls import path
from baseApp.api.views import registration

urlpatterns = [
    path('test/', registration, name='test')
]
