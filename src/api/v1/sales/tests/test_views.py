from datetime import timedelta
from http import HTTPStatus

from django.urls import reverse
from django.utils import timezone

from core.fixtures import TestSalesFixture
from sales.models import Sale


class TestSale(TestSalesFixture):
    def test_get_all_sales(self):
        response = self.user_client.get(reverse("sales-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json()), len(Sale.objects.all()))

    def test_sales_filter(self):
        response_1 = self.user_client.get(
            reverse("sales-list") + f"?sku_id={self.sku1.sku_id}"
        )
        self.assertEqual(
            len(response_1.data),
            len(Sale.objects.filter(sku__sku_id=self.sku1.sku_id)),
        )

        response_2 = self.user_client.get(
            reverse("sales-list") + f"?store_id={self.store1.store_id}"
        )
        self.assertEqual(
            len(response_2.data),
            len(Sale.objects.filter(store__store_id=self.store1.store_id)),
        )

    def test_post_sales(self):
        data = {
            "store_id": self.store1.store_id,
            "sku_id": self.sku6.sku_id,
            "date": timezone.now().date() - timedelta(days=1),
            "sales_type_id": 10,
            "sales_in_units": "1.000",
            "promo_sales_in_units": "1.000",
            "sales_in_rub": "103.00",
            "promo_sales_in_rub": "103.00",
        }
        response = self.user_client.post(reverse("sales-list"), data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_anon_clients_no_pasaran(self):
        response = self.anon_client.get(reverse("sales-list"))
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
