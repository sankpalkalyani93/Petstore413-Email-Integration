from django import forms 
from . models import Order

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)

class OrderCreateForm(forms.ModelForm): 
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'pincode', 'city']