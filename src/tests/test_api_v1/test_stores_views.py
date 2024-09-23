from http import HTTPStatus

from django.urls import reverse

from tests.fixtures import TestStoreFixture
from stores.models import Store


class TestSKU(TestStoreFixture):
    def test_get_all_stores(self):
        response = self.user_client.get(reverse("stores-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json()), len(Store.objects.all()))

    def test_store_search(self):
        param = "1"
        response = self.user_client.get(
            reverse("stores-list") + f"?search={param}"
        )
        self.assertEqual(
            len(response.json()),
            len(Store.objects.filter(store_id__icontains=param)),
        )

    def test_anon_client_has_no_access(self):
        response = self.anon_client.get(reverse("stores-list"))
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
