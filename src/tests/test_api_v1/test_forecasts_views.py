from datetime import timedelta

from http import HTTPStatus

from django.urls import reverse
from django.utils import timezone

from tests.fixtures import TestForecastsFixture


class TestForecasts(TestForecastsFixture):
    def test_get_all_forecasts(self):
        response = self.user_client.get(reverse("forecasts-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), len(self.frcst_query))

    def test_get_all_statistics(self):
        response = self.user_client.get(reverse("statistics-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_forecasts_filter(self):
        response_1 = self.user_client.get(
            reverse("forecasts-list") + f"?sku_id={self.sku1.sku_id}"
        )
        self.assertEqual(
            len(response_1.data),
            len(self.frcst_query.filter(sku__sku_id=self.sku1.sku_id)),
        )

        response_2 = self.user_client.get(
            reverse("forecasts-list") + f"?store_id={self.store1.store_id}"
        )
        self.assertEqual(
            len(response_2.data),
            len(self.frcst_query.filter(store__store_id=self.store1.store_id)),
        )

    def test_post_forecasts(self):
        forecast_data = {}
        for i in range(1, 15):
            forecast_data[str(timezone.now().date() + timedelta(days=i))] = i
        data = [
            {
                "store": self.store1.store_id,
                "sku": self.sku6.sku_id,
                "date": timezone.now().date(),
                "forecast_data": forecast_data,
            }
        ]
        response = self.user_client.post(
            reverse("load_forecasts-list"),
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_anon_clients_no_pasaran(self):
        response = self.anon_client.get(reverse("forecasts-list"))
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
