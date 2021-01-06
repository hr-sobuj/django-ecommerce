from django import forms
from App_Payment.models import Checkout

class SaveAddressForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ['address', 'zipcode', 'city', 'country']