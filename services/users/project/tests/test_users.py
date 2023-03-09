import json
import unittest
from project.api.models import User
from project import db
from project.tests.base import BaseTestCase


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get("/users/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("pong", data["message"])
        self.assertIn("success", data["status"])

    def test_add_user(self):
        """
        Ensure a new user can be added to the DB
        """

        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps(
                    {"username": "test user", "email": "testuser@mail.com"}
                ),
                content_type="application/json",
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn("testuser@mail.com was added", data["message"])
        self.assertIn("success", data["status"])

    def test_add_user_with_invalid_json(self):
        """
        Ensure error is thrown if JSON object is empty
        """

        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({}),
                content_type="application/json",
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid payload", data["message"])
        self.assertIn("fail", data["status"])

    def test_add_user_with_missing_json(self):
        """
        Ensure error is thrown if JSON object has missing keys
        """

        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({"username": "test user"}),
                content_type="application/json",
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid payload", data["message"])
        self.assertIn("fail", data["status"])

    def test_add_duplicate_user(self):
        """
        Ensure error is thrown if email already exists
        """

        with self.client:
            self.client.post(
                "/users",
                data=json.dumps(
                    {"username": "test user", "email": "testuser@mail.com"}
                ),
                content_type="application/json",
            )
            response = self.client.post(
                "/users",
                data=json.dumps(
                    {"username": "test user", "email": "testuser@mail.com"}
                ),
                content_type="application/json",
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("Email already in use", data["message"])
        self.assertIn("fail", data["status"])

    def test_single_user(self):
        """Ensure it returns a single user given an id"""
        user = add_user("test user", "testuser@mail.com")

        with self.client:
            response = self.client.get(f"/users/{user.id}")

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("test user", data["data"]["username"])
            self.assertIn("testuser@mail.com", data["data"]["email"])
            self.assertIn("success", data["status"])

    def test_single_user_no_id(self):
        """Ensure it returns an error when no id is provided"""

        with self.client:
            response = self.client.get(f"/users/hello")

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("User does not exist", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user_invalid_id(self):
        """Ensure it returns an error when user with provided is not found"""

        with self.client:
            response = self.client.get(f"/users/999999")

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("User does not exist", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user_invalid_id(self):
        """Ensure get all users returns a list if all users in the DB"""

        add_user("test user 1", "testuser1@gmail.com")
        add_user("test user 2", "testuser2@gmail.com")

        with self.client:
            response = self.client.get("/users")

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data["data"]["users"]), 2)
            self.assertIn("test user 1", data["data"]["users"][0]["username"])
            self.assertIn("test user 2", data["data"]["users"][1]["username"])
            self.assertIn("testuser1@gmail.com", data["data"]["users"][0]["email"])
            self.assertIn("testuser2@gmail.com", data["data"]["users"][1]["email"])
            self.assertIn("success", data["status"])


if __name__ == "__main__":
    unittest.main()
