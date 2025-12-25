# forms.py
from django import forms

from order.models import Order


class OrderForm(forms.ModelForm):
    """Форма для создания заказа."""

    class Meta:
        model = Order
        fields = ["name", "quantity", "description", "document"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Например: Запчасти для автомобиля"}
            ),
            "quantity": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Введите количество", "min": 1}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Подробно опишите товар...", "rows": 4}
            ),
            "document": forms.FileInput(attrs={"class": "form-control", "accept": ".pdf,.doc,.docx,.xls,.xlsx"}),
        }

    def __init__(self, *args, **kwargs):
        """Инициализация формы."""
        # Удаляем request из kwargs, если он есть
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        # Делаем description и document необязательными изначально
        self.fields["description"].required = False
        self.fields["document"].required = False

    def clean(self):
        """Кастомная валидация в зависимости от количества."""
        cleaned_data = super().clean()
        quantity = cleaned_data.get("quantity")
        description = cleaned_data.get("description")
        document = cleaned_data.get("document")

        if quantity == 1:
            # Для единичного заказа описание обязательно
            if not description or not description.strip():
                self.add_error("description", "Для единичного заказа необходимо заполнить описание")
        elif quantity and quantity > 1:
            # Для множественного заказа документ обязателен
            if not document:
                self.add_error("document", "Для множественного заказа необходимо прикрепить документ")

        return cleaned_data

    def clean_quantity(self):
        """Валидация количества."""
        quantity = self.cleaned_data.get("quantity")
        if quantity is None:
            raise forms.ValidationError("Это поле обязательно")
        if quantity < 1:
            raise forms.ValidationError("Количество должно быть не менее 1")
        return quantity

    def clean_name(self):
        """Валидация названия."""
        name = self.cleaned_data.get("name")
        if not name or not name.strip():
            raise forms.ValidationError("Название заказа обязательно")
        return name.strip()
