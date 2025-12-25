from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from order.models.order import Order


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Логин'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
    )


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации с username."""

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Настраиваем подсказки и стили
        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Придумайте логин"
        })
        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Пароль"
        })
        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Повторите пароль"
        })