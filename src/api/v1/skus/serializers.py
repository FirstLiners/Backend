from rest_framework import serializers

from skus.models import Category, Group, SubCategory, SKU


class GroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор для групп товаров.
    """

    class Meta:
        model = Group
        fields = ("group_id",)


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для категорий товаров.
    """

    class Meta:
        model = Category
        fields = ("cat_id",)


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для подкатегорий товаров.
    """

    class Meta:
        model = SubCategory
        fields = ("subcat_id",)


class SKUSerializer(serializers.ModelSerializer):
    """
    Сериализатор для товарных позиций.
    """

    group_id = serializers.CharField(
        source="subcategory.category.group.group_id"
    )
    cat_id = serializers.CharField(source="subcategory.category.cat_id")
    subcat_id = serializers.CharField(source="subcategory.subcat_id")

    class Meta:
        model = SKU
        fields = ["id", "sku_id", "uom", "group_id", "cat_id", "subcat_id"]
