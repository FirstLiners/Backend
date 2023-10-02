from django.db import models


class Store(models.Model):
    """
    Торговй центр.
    """

    store_id = models.CharField(
        "Иентификатор магазина", max_length=50, unique=True, db_index=True
    )
    city_id = models.CharField("Идентификатор города", max_length=50)
    division_code = models.CharField(
        "Идентификатор дивизиона",
        max_length=50,
    )
    type_format_id = models.PositiveIntegerField(
        "Идентификатор формата магазина",
    )
    type_loc_id = models.PositiveIntegerField(
        "Тип локации магазина",
    )
    type_size_id = models.PositiveIntegerField(
        "Тип размера магазина",
    )
    is_active = models.PositiveIntegerField(
        "Активени ли магазин",
    )

    class Meta:
        verbose_name = "Торговый центр"
        verbose_name_plural = "Торговые центры"
        ordering = ["store_id"]

    def __str__(self):
        return self.store_id
