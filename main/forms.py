from django import forms
from .models import ContactMessage
from .models import Product

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'message']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'phone_number': 'Teléfono',
            'email': 'Correo',
            'message': 'Mensaje',
        }




class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'type', 'price', 'image', 'stock']

