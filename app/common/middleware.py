from django.shortcuts import redirect
from django.urls import reverse


class AuthRequiredMiddleware:
    """Авторизованный доступ к апи.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in [
            "/login/",
            "/registration/",
            "/admin/",
            "/admin/login/",
        ]:
            return self.get_response(request)

        if not request.user.is_authenticated:
            return redirect("login")

        return self.get_response(request)
