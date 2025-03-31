from itertools import chain

from django import forms
from .models import Person, Educator, Employee, Teacher
from django.db.models import Q

class LoginForm(forms.Form):
    email = forms.EmailField(label="Courriel", required=True)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        # Vérifie que les deux champs sont valides
        if email and password:
            educator_queryset = Educator.objects.filter(Q(password=password) & Q(employee_email=email))
            teacher_queryset = Teacher.objects.filter(Q(password=password) & Q(employee_email=email))

            # Combinez les résultats avec `chain`
            result = list(chain(educator_queryset, teacher_queryset))
            if len(result) != 1:
                raise forms.ValidationError("Adresse de courriel ou mot de passe erroné.")
        return cleaned_data
