from django.contrib import admin
from django.utils import timezone

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Заказ."""

    list_display = (
        "id",
        "user",
        "name",
        "status",
    )
    list_filter = ("status",)
    search_fields = (
        "name",
        "user__username",
    )

    def save_model(self, request, obj, form, change):
        if change and "status" in form.changed_data:
            if obj.status == Order.StatusTypes.READY:
                obj.completion_date = timezone.now()
        elif not change and obj.status == Order.StatusTypes.READY:
            obj.completion_date = timezone.now()

        super().save_model(request, obj, form, change)
