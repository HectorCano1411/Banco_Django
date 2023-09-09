# from django import forms

# class LoginForm(forms.Form):
#     rut = forms.CharField(max_length=12, label='RUT de Usuario')
#     password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

from django import forms
from django.core.exceptions import ValidationError
import re

class RegistroFormulario(forms.Form):
    # Otros campos del formulario

    def validate_password_complexity(self, password):
        if not re.search(r'[A-Z]', password):
            raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("La contraseña debe contener al menos una letra minúscula.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("La contraseña debe contener al menos un número.")
        if not re.search(r'[!@#$%^&*()_+{}[\]:;<>,.?~\\-]', password):
            raise ValidationError("La contraseña debe contener al menos un carácter especial.")

    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
        min_length=8, 
        validators=[validate_password_complexity]  
    )
