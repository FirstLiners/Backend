from http import HTTPStatus

from django.contrib.auth import get_user_model

from tests.fixtures import TestUserFixture

User = get_user_model()


class TestUser(TestUserFixture):
    def test_get_token(self):
        email = "user@foo.com"
        password = "pass"
        User.objects.create_user(email=email, password=password)
        body = {"email": email, "password": password}
        response = self.anon_client.post(
            "/api/v1/users/token/", data=body, format="json"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)
