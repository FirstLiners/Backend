from http import HTTPStatus

from django.urls import reverse

from core.fixtures import TestSKUFixture
from skus.models import Category, Group, SKU, SubCategory


class TestSKU(TestSKUFixture):
    def test_get_all_groups(self):
        response = self.user_client.get(reverse("groups-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json()), len(Group.objects.all()))

    def test_get_all_categories(self):
        response = self.user_client.get(reverse("categories-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json()), len(Category.objects.all()))

    def test_get_all_subcategories(self):
        response = self.user_client.get(reverse("subcategories-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json()), len(SubCategory.objects.all()))

    def test_get_all_skus(self):
        response = self.user_client.get(reverse("skus-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json()), len(SKU.objects.all()))

    def test_group_search(self):
        param = "1"
        response = self.user_client.get(
            reverse("groups-list") + f"?search={param}"
        )
        self.assertEqual(
            len(response.json()),
            len(Group.objects.filter(group_id__icontains=param)),
        )

    def test_category_search(self):
        param = "1"
        response = self.user_client.get(
            reverse("categories-list") + f"?search={param}"
        )
        self.assertEqual(
            len(response.json()),
            len(Category.objects.filter(cat_id__icontains=param)),
        )

    def test_category_filter(self):
        response = self.user_client.get(
            reverse("categories-list") + f"?group_id={self.group1.group_id}"
        )
        self.assertEqual(
            len(response.json()),
            len(Category.objects.filter(group__group_id=self.group1.group_id)),
        )

    def test_subcategory_search(self):
        param = "1"
        response = self.user_client.get(
            reverse("subcategories-list") + f"?search={param}"
        )
        self.assertEqual(
            len(response.json()),
            len(SubCategory.objects.filter(subcat_id__icontains=param)),
        )

    def test_subcategory_filter(self):
        response = self.user_client.get(
            reverse("subcategories-list") + f"?group_id={self.group1.group_id}"
        )
        self.assertEqual(
            len(response.json()),
            len(
                SubCategory.objects.filter(
                    category__group__group_id=self.group1.group_id
                )
            ),
        )

    def test_sku_search(self):
        param = "1"
        response = self.user_client.get(
            reverse("skus-list") + f"?search={param}"
        )
        self.assertEqual(
            len(response.json()),
            len(SKU.objects.filter(sku_id__icontains=param)),
        )

    def test_sku_filter(self):
        response = self.user_client.get(
            reverse("skus-list") + f"?group_id={self.group1.group_id}"
        )
        self.assertEqual(
            len(response.json()),
            len(
                SKU.objects.filter(
                    subcategory__category__group__group_id=self.group1.group_id
                )
            ),
        )

        response_2 = self.user_client.get(
            reverse("skus-list") + f"?cat_id={self.cat11.cat_id}"
        )
        self.assertEqual(
            len(response_2.json()),
            len(
                SKU.objects.filter(
                    subcategory__category__cat_id=self.cat11.cat_id
                )
            ),
        )

    def test_anon_client_has_no_access(self):
        response = self.anon_client.get(reverse("groups-list"))
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        response2 = self.anon_client.get(reverse("categories-list"))
        self.assertEqual(response2.status_code, HTTPStatus.UNAUTHORIZED)

        response3 = self.anon_client.get(reverse("subcategories-list"))
        self.assertEqual(response3.status_code, HTTPStatus.UNAUTHORIZED)

        response4 = self.anon_client.get(reverse("skus-list"))
        self.assertEqual(response4.status_code, HTTPStatus.UNAUTHORIZED)
