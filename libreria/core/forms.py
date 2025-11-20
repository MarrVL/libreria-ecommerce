# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# Obtiene el modelo de usuario activo (generalmente User)
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """
    Formulario de registro personalizado que añade el campo 'email'.
    """
    email = forms.EmailField(
        label="Correo Electrónico",
        max_length=254,
        # Asegúrate de que el campo sea obligatorio
        required=True, 
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # Define el orden de los campos para que coincida con tu plantilla
        fields = ('username', 'email') + UserCreationForm.Meta.fields[2:]

    def save(self, commit=True):
        # Asegura que el email se guarde en el objeto de usuario
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user