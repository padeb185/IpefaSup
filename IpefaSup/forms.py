from django import forms
from .models import Person, Educator, Employee


class LoginForm(forms.Form):
    email = forms.EmailField(label="Courriel", required=True)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        # Vérifie que les deux champs sont valides
        if email and password:
            result = Educator.objects.filter(password=password, employee_email=email)
            if result.count() != 1:
                raise forms.ValidationError("Adresse de courriel ou mot de passe erroné.")

        return cleaned_data
