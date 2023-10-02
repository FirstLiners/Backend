from django.db import models


class SaleForecastManager(models.Manager):
    """
    Менеджер для моделей продаж и прогнозов.
    """

    def get_queryset(self):
        return super().get_queryset().select_related(
            "store",
            "sku",
            "sku__subcategory",
            "sku__subcategory__category",
            "sku__subcategory__category__group",
        )
