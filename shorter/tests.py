from django.test import TestCase, Client
from .models import Links

class RedirectServiceTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.link = Links.objects.create(
            redirect_link="https://google.com",
            token="testtoken"
        )

    def test_update_link_preserves_token(self):
        old_token = self.link.token
        response = self.client.patch(
            f"/api/v1/{self.link.id}/",
            data={"redirect_link": "https://youtube.com", "token": ""},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.link.refresh_from_db()
        self.assertEqual(self.link.token, old_token)
        self.assertEqual(self.link.redirect_link, "https://youtube.com")


    def test_expired_without_expiration_time(self):
        self.assertFalse(self.link.expired())

    def test_statistics(self):
        response = self.client.get(f"/api/v1/statistics/{self.link.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_clicks", response.json())
        self.assertIn("uniques_clicks", response.json())

