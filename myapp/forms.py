from django.forms import ModelForm
from .models import productsrequests

class createRequestForm(ModelForm):
    class Meta:
        model = productsrequests
        fields = ("productname","description")