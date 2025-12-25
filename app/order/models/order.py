from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    """Заказ.
    """

    class StatusTypes:

        CREATED = "CREATED"
        PROCESSING = "PROCESSING"
        ASSEMBLING = "ASSEMBLING"
        DELIVERING = "DELIVERING"
        READY = "READY"

        CHOICES = (
            (CREATED, _("Создан")),
            (PROCESSING, _("Обрабатывается")),
            (ASSEMBLING, _("Собирается")),
            (DELIVERING, _("Доставляется")),
            (READY, _("Готов")),
        )

    name = models.CharField(
        verbose_name=_("Наименование заказа"),
        max_length=256,
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_("Количество"),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Описание"),
    )
    document = models.FileField(
        verbose_name=_("Документ"),
        upload_to="order_documents/",
        blank=True,
        null=True,
    )
    status = models.CharField(
        verbose_name=_("Статус"),
        max_length=32,
        choices=StatusTypes.CHOICES,
        default=StatusTypes.CREATED,
    )
    completion_data = models.DateTimeField(
        verbose_name=_("Дата готовности"),
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания записи"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Дата изменения записи"),
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")

    def __str__(self):
        return f"Заказ №{self.id} - {self.name}"
