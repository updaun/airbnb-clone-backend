from rest_framework.test import APITestCase
from .models import Amenity


class TestAmenities(APITestCase):

    NAME = "Amenity Test"
    DESC = "Amenity Test Description"

    URL = "/api/v1/rooms/amenities/"

    def setUp(self):
        Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_all_amenities(self):

        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 200, "Status code isn't 200.")
        self.assertIsInstance(data, list, "Data isn't a list.")
        self.assertEqual(len(data), 1, "Data length isn't 1.")
        self.assertEqual(data[0]["name"], self.NAME, "Name isn't equal.")
        self.assertEqual(data[0]["description"], self.DESC, "Description isn't equal.")

    def test_create_amenity(self):

        new_amenity_name = "New Amenity"
        new_amenity_desc = "New Amenity Description"

        response = self.client.post(
            self.URL, data={"name": new_amenity_name, "description": new_amenity_desc}
        )

        data = response.json()

        self.assertEqual(response.status_code, 200, "Status code isn't 200.")
        self.assertIsInstance(data, dict, "Data isn't a dict.")
        self.assertEqual(data["name"], new_amenity_name, "Name isn't equal.")
        self.assertEqual(
            data["description"], new_amenity_desc, "Description isn't equal."
        )

        response = self.client.post(self.URL)
        data = response.json()
        self.assertEqual(response.status_code, 400, "Status code isn't 400.")
        self.assertIn("name", data, "Name isn't in data.")
