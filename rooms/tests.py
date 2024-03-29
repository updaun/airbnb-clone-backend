from rest_framework.test import APITestCase
from .models import Amenity
from users.models import User


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


class TestAmenity(APITestCase):

    NAME = "Test Amenity"
    DESC = "Test Amenity Description"

    def setUp(self):
        self.amenity = Amenity.objects.create(name=self.NAME, description=self.DESC)

    def test_get_amenity_not_found(self):
        response = self.client.get(f"/api/v1/rooms/amenities/2")

        self.assertEqual(response.status_code, 404, "Status code isn't 404.")

    def test_get_amenity(self):

        response = self.client.get(f"/api/v1/rooms/amenities/{self.amenity.pk}")
        data = response.json()

        self.assertEqual(response.status_code, 200, "Status code isn't 200.")
        self.assertIsInstance(data, dict, "Data isn't a dict.")
        self.assertEqual(data["name"], self.NAME, "Name isn't equal.")
        self.assertEqual(data["description"], self.DESC, "Description isn't equal.")

    def test_put_amenity(self):
        new_name = "New Name"
        new_desc = "New Description"

        response = self.client.put(
            f"/api/v1/rooms/amenities/{self.amenity.pk}",
            data={"name": new_name, "description": new_desc},
        )

        data = response.json()

        self.assertEqual(response.status_code, 200, "Status code isn't 200.")
        self.assertIsInstance(data, dict, "Data isn't a dict.")
        self.assertEqual(data["name"], new_name, "Name isn't equal.")
        self.assertEqual(data["description"], new_desc, "Description isn't equal.")

    def test_delete_amenity(self):
        response = self.client.delete(f"/api/v1/rooms/amenities/{self.amenity.pk}")
        self.assertEqual(response.status_code, 204, "Status code isn't 204.")


class TestRooms(APITestCase):
    def setUp(self):
        user = User.objects.create(username="test")
        user.set_password("password1234!")
        user.save()
        self.user = user

    def test_create_room(self):

        response = self.client.post("/api/v1/rooms/")

        self.assertEqual(response.status_code, 403, "Status code isn't 403.")

        # self.client.login(
        #     username="test",
        #     password="password1234!"
        # )

        self.client.force_login(self.user)

        response = self.client.post("/api/v1/rooms/")
