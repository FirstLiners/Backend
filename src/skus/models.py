from django.db import models

from .managers import CategoryManager, SKUManager, SubCategoryManager


class Group(models.Model):
    """
    Группа товара.
    """

    group_id = models.CharField(
        "Идентификатор группы товара",
        max_length=50,
        db_index=True,
        unique=True,
    )

    class Meta:
        verbose_name = "Группа товара"
        verbose_name_plural = "Группы товаров"
        ordering = [
            "group_id",
        ]

    def __str__(self):
        return self.group_id


class Category(models.Model):
    """
    Категория товара.
    """

    cat_id = models.CharField(
        "Идентификатор категории товара",
        max_length=50,
        db_index=True,
        unique=True,
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.PROTECT,
        verbose_name="Группа",
        related_name="categories",
    )

    objects = CategoryManager()

    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"
        ordering = [
            "cat_id",
        ]

    def __str__(self):
        return self.cat_id


class SubCategory(models.Model):
    """
    Подкатегория товара.
    """

    subcat_id = models.CharField(
        "Идентификатор подкатегории товара",
        max_length=50,
        db_index=True,
        unique=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="Категория",
        related_name="subcategories",
    )

    objects = SubCategoryManager()

    class Meta:
        verbose_name = "Подкатегория товара"
        verbose_name_plural = "Подкатегории товаров"
        ordering = [
            "subcat_id",
        ]

    def __str__(self):
        return self.subcat_id


class SKU(models.Model):
    """
    Товарная позиция.
    """

    sku_id = models.CharField(
        "Идентификатор товарной позиции",
        max_length=50,
        db_index=True,
        unique=True,
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.PROTECT,
        verbose_name="Подкатегория",
        related_name="skus",
    )

    uom = models.PositiveIntegerField("Идентификатор единицы измерения")

    objects = SKUManager()

    class Meta:
        verbose_name = "Товарная позиция"
        verbose_name_plural = "Товарные позиции"
        ordering = [
            "sku_id",
        ]

    def __str__(self):
        return self.sku_id
