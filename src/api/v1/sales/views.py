from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from sales.models import Sale

from .serializers import SaleGetSerializer


@extend_schema(tags=["Sales"])
@extend_schema_view(
    list=extend_schema(summary="Информация о продажах товара в ТЦ"),
)
class SaleGetViewset(ListModelMixin, GenericViewSet):
    """
    Вьюсет для получения списка продаж.
    Принимает параметры "sku_id" и "store_id" (несколько параметров передавать
    через запятую) и выводит продажи по выбранным товарам и ТЦ соответственно.
    """

    def get_queryset(self):
        queryset = Sale.objects.all()
        if self.request.method == "GET":
            params = self.request.query_params
            store_id = params.get("store_id", None)
            sku_id = params.get("sku_id", None)
            print(sku_id, store_id)
            if store_id:
                queryset = queryset.filter(
                    store__store_id__in=store_id.split(",")
                )
            if sku_id:
                queryset = queryset.filter(sku__sku_id__in=sku_id.split(","))
        return queryset
    serializer_class = SaleGetSerializer
