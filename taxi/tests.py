from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer
from django.contrib.auth import get_user_model


class SearchTests(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        self.car = Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer
        )
        self.driver = Driver.objects.create(
            username="john_doe",
            first_name="John",
            last_name="Doe",
            license_number="123456",
        )

    def test_driver_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?q=john_doe"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_doe")

    def test_car_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?q=Model S"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Model S")

    def test_manufacturer_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?q=Tesla"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tesla")

    def test_no_search_results(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?q=nonexistent_user"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No drivers found")

    def test_search_with_empty_query(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver.username)


class TaxiViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer
        )

    def test_index_view_requires_login(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    def test_manufacturer_list_view_authenticated(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_car_create_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(response.status_code, 200)
