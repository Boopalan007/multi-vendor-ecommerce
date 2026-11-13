
from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User
from products.models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            'name',
            'category',
            'description',
            'price',
            'stock',
            'image',
            'is_available'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter product name'
            }),

            'category': forms.Select(),

            'description': forms.Textarea(attrs={
                'placeholder': 'Enter product description',
                'rows': 4
            }),

            'price': forms.NumberInput(attrs={
                'placeholder': 'Enter product price',
                'step': '0.01'
            }),

            'stock': forms.NumberInput(attrs={
                'placeholder': 'Enter available stock'
            }),
        }


class VendorRegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)
    business_name = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=100)
    description = forms.CharField(
        widget=forms.Textarea,
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def save(self, commit=True):

        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = 'vendor'

        if commit:
            user.save()

        return user
