from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.db.models import Q

from order.forms.order import OrderForm
from order.models.order import Order

class OrderListView(LoginRequiredMixin, ListView):
    """Список заказов."""
    model = Order
    template_name = "order/list.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтрация по пользователю (если не админ)
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        # Фильтрация по статусу
        status_filter = self.request.GET.get("status", "")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Поиск по наименованию
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statuses"] = dict(Order.StatusTypes.CHOICES)
        context["current_status"] = self.request.GET.get("status", "")
        context["search_query"] = self.request.GET.get("search", "")

        # Статистика по статусам
        if not self.request.user.is_staff:
            user_orders = Order.objects.filter(user=self.request.user)
        else:
            user_orders = Order.objects.all()

        context["stats"] = {
            "total": user_orders.count(),
            "created": user_orders.filter(status=Order.StatusTypes.CREATED).count(),
            "processing": user_orders.filter(status=Order.StatusTypes.PROCESSING).count(),
            "assembling": user_orders.filter(status=Order.StatusTypes.ASSEMBLING).count(),
            "delivering": user_orders.filter(status=Order.StatusTypes.DELIVERING).count(),
            "ready": user_orders.filter(status=Order.StatusTypes.READY).count(),
        }

        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    """Детальный просмотр заказа."""
    model = Order
    template_name = "order/detail.html"
    context_object_name = "order"
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        order = super().get_object(queryset)
        # Проверка прав доступа
        if not self.request.user.is_staff and order.user != self.request.user:
            from django.http import Http404
            raise Http404("Заказ не найден")
        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statuses"] = dict(Order.StatusTypes.CHOICES)

        # Индекс статуса для прогресс-бара
        status_order = [
            Order.StatusTypes.CREATED,
            Order.StatusTypes.PROCESSING,
            Order.StatusTypes.ASSEMBLING,
            Order.StatusTypes.DELIVERING,
            Order.StatusTypes.READY,
        ]
        try:
            context["status_index"] = status_order.index(self.object.status)
        except ValueError:
            context["status_index"] = 0

        return context


class OrderCreateView(LoginRequiredMixin, CreateView):
    """Создание нового заказа."""
    model = Order
    form_class = OrderForm
    template_name = 'order/create.html'
    success_url = reverse_lazy('order_list')

    def get_form_kwargs(self):
        """Передаем request в форму."""
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request  # Теперь форма принимает request
        return kwargs

    def form_valid(self, form):
        """Автоматически привязываем заказ к текущему пользователю."""
        form.instance.user = self.request.user
        form.instance.status = Order.StatusTypes.CREATED

        # Сохраняем файл документа, если он есть
        if form.cleaned_data.get('document'):
            document = form.cleaned_data['document']
            form.instance.document = document

        response = super().form_valid(form)
        messages.success(self.request, 'Заказ успешно создан!')
        return response

    def form_invalid(self, form):
        """Обработка невалидной формы."""
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)