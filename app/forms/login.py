from django import forms

from django.contrib.auth.forms import AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):
    # Personalize conforme necessário
    email = forms.EmailField(widget=forms.EmailInput(attrs={"autofocus": True}))
