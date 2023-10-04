from django_filters import (
    FilterSet,
    ModelChoiceFilter,
    ModelMultipleChoiceFilter,
)

from forecasts.models import Forecast
from stores.models import Store
from skus.models import Category, Group, SubCategory, SKU


class ForecastFilter(FilterSet):
    """
    Фильтр для прогнозов.
    """

    store_id = ModelChoiceFilter(
        field_name="store__store_id",
        to_field_name="store_id",
        queryset=Store.objects.all(),
    )

    sku_id = ModelMultipleChoiceFilter(
        field_name="sku__sku_id",
        to_field_name="sku_id",
        queryset=SKU.objects.all(),
    )

    subcat_id = ModelMultipleChoiceFilter(
        field_name="sku__subcategory__subcat_id",
        to_field_name="subcat_id",
        queryset=SubCategory.objects.all(),
    )

    cat_id = ModelMultipleChoiceFilter(
        field_name="sku__subcategory__category__cat_id",
        to_field_name="cat_id",
        queryset=Category.objects.all(),
    )

    group_id = ModelMultipleChoiceFilter(
        field_name="sku__subcategory__category__group__group_id",
        to_field_name="group_id",
        queryset=Group.objects.all(),
    )

    class Meta:
        model = Forecast
        fields = [
            "store_id",
            "sku_id",
            "subcat_id",
            "cat_id",
            "group_id",
        ]


class StatisticsFilter(ForecastFilter):
    """
    Фильтр для статистики по прогнозам.
    """

    store_id = ModelMultipleChoiceFilter(
        field_name="store__store_id",
        to_field_name="store_id",
        queryset=Store.objects.all(),
    )
