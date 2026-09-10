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

    def test_update_link_preserves_redirect_link_when_empty(self):
        old_url = self.link.redirect_link
        response = self.client.patch(
            f"/api/v1/{self.link.id}/",
            data={"max_uniques_cliques": 50, "redirect_link": ""},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.link.refresh_from_db()
        self.assertEqual(self.link.redirect_link, old_url)
        self.assertEqual(self.link.max_uniques_cliques, 50)


    def test_expired_without_expiration_time(self):
        self.assertFalse(self.link.expired())

    def test_statistics(self):
        response = self.client.get(f"/api/v1/statistics/{self.link.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_clicks", response.json())
        self.assertIn("uniques_clicks", response.json())

    def test_update_link_expiration_time(self):
        response = self.client.patch(
            f"/api/v1/{self.link.id}/",
            data={"expiration_time": "02:00:00"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.link.refresh_from_db()
        self.assertIsNotNone(self.link.expiration_time)
        self.assertEqual(self.link.expiration_time.total_seconds(), 7200)


