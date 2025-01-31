from django.test import TestCase
from django.urls import reverse
from .models import Driver, Car, Manufacturer


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
