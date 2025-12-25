from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from order.forms.user import CustomUserCreationForm, LoginForm


class RegistrationView(CreateView):
    """Регистрация нового пользователя."""

    form_class = CustomUserCreationForm
    template_name = "user/registration.html"
    success_url = reverse_lazy("order_list")

    def form_valid(self, form):
        """Автоматический вход после регистрации."""
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response


class LoginView(View):
    """Авторизация в системе."""

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("order_list")
        form = LoginForm()
        return render(request, "user/login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("order_list")

        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("order_list")
        return render(request, "user/login.html", {"form": form})


class LogoutView(LoginRequiredMixin, View):
    """Выход из системы."""

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")
