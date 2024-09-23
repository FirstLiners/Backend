from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from api.v1.serializers import StoreSerializer
from stores.models import Store


@extend_schema(tags=["Stores"])
@extend_schema_view(
    list=extend_schema(summary="Список торговых центров"),
)
class StoreViewSet(ListModelMixin, GenericViewSet):
    """
    Вьюсет для торговых центров.
    """

    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["store_id"]
