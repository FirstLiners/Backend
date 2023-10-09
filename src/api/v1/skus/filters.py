from django_filters import (
    FilterSet,
    ModelMultipleChoiceFilter,
)

from skus.models import Category, Group, SubCategory, SKU


class CategoryFilter(FilterSet):
    """
    Фильтр для категорий.
    """

    group_id = ModelMultipleChoiceFilter(
        field_name="group__group_id",
        to_field_name="group_id",
        queryset=Group.objects.all(),
    )

    class Meta:
        model = Category
        fields = [
            "group_id",
        ]


class SubCategoryFilter(FilterSet):
    """
    Фильтр для подкатегорий.
    """

    group_id = ModelMultipleChoiceFilter(
        field_name="category__group__group_id",
        to_field_name="group_id",
        queryset=Group.objects.all(),
    )

    cat_id = ModelMultipleChoiceFilter(
        field_name="category__cat_id",
        to_field_name="cat_id",
        queryset=Category.objects.all(),
    )

    class Meta:
        model = SubCategory
        fields = [
            "group_id",
            "cat_id",
        ]


class SkuFilter(FilterSet):
    """
    Фильтр для товарных единиц.
    """

    group_id = ModelMultipleChoiceFilter(
        field_name="subcategory__category__group__group_id",
        to_field_name="group_id",
        queryset=Group.objects.all(),
    )

    cat_id = ModelMultipleChoiceFilter(
        field_name="subcategory__category__cat_id",
        to_field_name="cat_id",
        queryset=Category.objects.all(),
    )

    subcat_id = ModelMultipleChoiceFilter(
        field_name="subcategory__subcat_id",
        to_field_name="subcat_id",
        queryset=SubCategory.objects.all(),
    )

    class Meta:
        model = SKU
        fields = [
            "group_id",
            "cat_id",
            "subcat_id"
        ]
