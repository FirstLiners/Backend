from django.db import models

from core.managers import SaleForecastManager
from skus.models import SKU
from stores.models import Store


class Sale(models.Model):
    """
    Информация о продаже товара в супермаркете за сутки.
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
        "Дата продажи",
        auto_now_add=False,
    )
    sales_type_id = models.PositiveIntegerField(
        "Наличие промо",
    )
    sales_in_units = models.DecimalField(
        "Количество проданных товаров",
        max_digits=8,
        decimal_places=3,
    )
    promo_sales_in_units = models.DecimalField(
        "Количество проданных товаров c промо",
        max_digits=8,
        decimal_places=3,
    )
    sales_in_rub = models.DecimalField(
        "Стоимость проданных товаров, руб.",
        max_digits=9,
        decimal_places=2,
    )
    promo_sales_in_rub = models.DecimalField(
        "Стоимость проданных товаров с промо, руб.",
        max_digits=9,
        decimal_places=2,
    )

    objects = SaleForecastManager()

    class Meta:
        verbose_name = "Продажа товара в супермаркете за сутки"
        verbose_name_plural = "Продажи товаров в супермаркетах за посуточно"
        ordering = ["store", "sku", "date"]
        index_together = [
            ["store", "sku", "date"],
        ]
        default_related_name = "sales"
        constraints = [
            models.UniqueConstraint(
                fields=["store", "sku", "date"],
                name="double sale info (unique)",
            )
        ]

    def __str__(self):
        return f"{self.date}: {self.store.store_id} - {self.sku.sku_id}"
