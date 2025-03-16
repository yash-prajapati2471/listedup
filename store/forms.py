from django import forms
from .models import product

class ProductForm(forms.ModelForm):
    class Meta:
        model = product
        exclude = ['seller', 'slug', 'is_active', 'creates_at']

        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'product_detail': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'product_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_hideprice': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_image': forms.FileInput(attrs={'class': 'form-control'}),
            'product_image1': forms.FileInput(attrs={'class': 'form-control'}),
            'product_image2': forms.FileInput(attrs={'class': 'form-control'}),
            'product_image3': forms.FileInput(attrs={'class': 'form-control'}),
        }
