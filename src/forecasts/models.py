from django.db import models

from core.managers import SaleForecastManager
from skus.models import SKU
from stores.models import Store


class Forecast(models.Model):
    """
    Прогноз прожаж товара в супермаркете на 14 дней.
    """

    store = models.ForeignKey(
        Store,
        on_delete=models.PROTECT,
        verbose_name="Торговый центр",
    )
    sku = models.ForeignKey(
        SKU,
        on_delete=models.PROTECT,
        verbose_name="Товар",
    )
    date = models.DateField(
        "Дата прогноза",
        auto_now_add=False,
    )
    forecast_data = models.JSONField("Прогноз продаж по датам.", default=dict)

    objects = SaleForecastManager()

    class Meta:
        verbose_name = "Пргноз продаж товара в супермаркете"
        verbose_name_plural = "Пргноз продаж товаров в супермаркетах"
        ordering = ["store", "sku", "date"]
        index_together = [
            ["store", "sku", "date"],
        ]
        default_related_name = "forecasts"
        constraints = [
            models.UniqueConstraint(
                fields=["store", "sku", "date"],
                name="double forecast (unique)",
            )
        ]

    def __str__(self):
        return f"{self.date}: {self.store.store_id} - {self.sku.sku_id}"
