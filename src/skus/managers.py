from django.db import models


class CategoryManager(models.Manager):
    """
    Менеджер для модели категорий.
    """

    def get_queryset(self):
        return super().get_queryset().select_related("group")


class SubCategoryManager(models.Manager):
    """
    Менеджер для модели подкатегорий.
    """

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("category", "category__group")
        )


class SKUManager(models.Manager):
    """
    Менеджер для модели товарных позиций.
    """

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                "subcategory",
                "subcategory__category",
                "subcategory__category__group",
            )
        )
