
from django.forms import ModelForm
from baseApp.databases.models import Account

from django import forms
from baseApp.databases.models import FileUpload

class DocumentForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('description', 'file', )
class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ("username", "password")
