from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiExample,
)
from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from sales.models import Sale

from .serializers import SaleSerializer, SaleCreateSerializer


@extend_schema(tags=["Sales"])
@extend_schema_view(
    list=extend_schema(summary="Информация о продажах товара в ТЦ"),
    create=extend_schema(
        summary="Загрузка данных по продажам товаров",
        examples=[
            OpenApiExample(
                "Пример загрузки данных",
                value=[
                    {
                        "store_id": "084a8a9aa8cced9175bd07bc44998e75",
                        "sku_id": "88feeeb024d3f69da7322d76b7b53744",
                        "date": "2022-03-30",
                        "sales_type_id": 1,
                        "sales_in_units": "1.000",
                        "promo_sales_in_units": "1.000",
                        "sales_in_rub": "103.00",
                        "promo_sales_in_rub": "103.00",
                    },
                ],
                status_codes=[str(status.HTTP_201_CREATED)],
            ),
        ],
    ),
)
class SaleGetViewset(ListModelMixin, CreateModelMixin, GenericViewSet):
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
            if store_id:
                queryset = queryset.filter(
                    store__store_id__in=store_id.split(",")
                )
            if sku_id:
                queryset = queryset.filter(sku__sku_id__in=sku_id.split(","))
        return queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return SaleCreateSerializer
        return SaleSerializer

    def create(self, request, *args, **kwargs):
        serializer = SaleCreateSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
