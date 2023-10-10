from django.db import models

from core.managers import SaleForecastManager
from skus.models import SKU
from stores.models import Store


class Forecast(models.Model):
    """
    Прогноз прожаж товара в супермаркете на 14 дней.
    Поля next_day_real_sale и next_day_forecast добавлены для
    сокращения времени построения отчета по статистике прогнозов.
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
    next_day_real_sale = models.PositiveIntegerField(
        "Реальные продажи на следующий день",
        null=True,
        default=0,
    )
    next_day_forecast = models.PositiveIntegerField(
        "Прогноз на следующий день"
    )

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


class StoreSKU(models.Model):
    """
    Модель для связи магазинов и товаров.
    """

    store = models.ForeignKey(
        Store,
        on_delete=models.PROTECT,
        related_name="skus",
        verbose_name="Торговый центр",
    )
    sku = models.ForeignKey(
        SKU,
        on_delete=models.PROTECT,
        related_name="stores",
        verbose_name="Товар",
    )
    is_active = models.BooleanField(
        "Нужен прогноз",
        default=True,
    )

    objects = SaleForecastManager()

    class Meta:
        verbose_name = "Товар магазина"
        verbose_name_plural = "Товары магазинов"
        ordering = ["store", "sku"]
        index_together = [
            ["store", "sku"],
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["store", "sku"],
                name="double store&sku (unique)",
            )
        ]

    def __str__(self):
        return f"{self.store} - {self.sku}"
