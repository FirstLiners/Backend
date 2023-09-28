from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from skus.models import Category, Group, SKU, SubCategory

from .serializers import (CategorySerializer, GroupSerializer, SKUSerializer,
                          SubCategorySerializer)


@extend_schema(tags=["SKUs"])
@extend_schema_view(
    list=extend_schema(summary="Список товарных позиций"),
)
class SKUViewSet(ListModelMixin, GenericViewSet):
    """
    Вьюсет для товарных позиций.
    """
    queryset = SKU.objects.all()
    serializer_class = SKUSerializer


@extend_schema(tags=["Groups"])
@extend_schema_view(
    list=extend_schema(summary="Список групп товаров"),
)
class GroupViewSet(ListModelMixin, GenericViewSet):
    """
    Вьюсет для групп товаров.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@extend_schema(tags=["Categories"])
@extend_schema_view(
    list=extend_schema(summary="Список категорий товаров"),
)
class CategoryViewSet(ListModelMixin, GenericViewSet):
    """
    Вьюсет для категорий товаров.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema(tags=["Subcategories"])
@extend_schema_view(
    list=extend_schema(summary="Список подкатегорий товаров"),
)
class SubCategoryViewSet(ListModelMixin, GenericViewSet):
    """
    Вьюсет для подкатегорий товаров.
    """
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
