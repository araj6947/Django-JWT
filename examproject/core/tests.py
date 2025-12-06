from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User, Role, Gadget


class TestLogin(APITestCase):

    def setUp(self):
        print("\n====== Setting Up Test Data ======\n")

        self.client = APIClient()

        # roles
        self.admin_role = Role.objects.create(roleName="admin")
        self.user_role = Role.objects.create(roleName="user")

        # admin user
        self.admin = User.objects.create(
            email="admin@mail.com",
            username="admin",
            password="adminpass",
            role=self.admin_role
        )

        # user for gadget tests
        self.user1 = User.objects.create(
            email="u1@mail.com",
            username="u1",
            password="pass1",
            role=self.user_role
        )

        self.user2 = User.objects.create(
            email="u2@mail.com",
            username="u2",
            password="pass2",
            role=self.user_role
        )

        # Gadgets for user1
        Gadget.objects.create(
            name="Phone",
            description="Phone test",
            price=100,
            created_by=self.user1
        )
        Gadget.objects.create(
            name="Laptop",
            description="Laptop test",
            price=200,
            created_by=self.user1
        )

    # helper
    def login(self, email, password):
        url = reverse("login")
        print(f"\n---- Trying login with ----\nEmail: {email}\nPassword: {password}\n")
        return self.client.post(url, {"email": email, "password": password}, format="json")

    # -------- LOGIN TESTS --------

    def test_login_success(self):
        print("\n======= Test: Login Success =======\n")
        res = self.login("admin@mail.com", "adminpass")
        print("Response:", res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("token", res.data)
        self.assertEqual(res.data["name"], "admin")

    def test_login_failure(self):
        print("\n======= Test: Login Wrong Password =======\n")
        res = self.login("admin@mail.com", "wrong")
        print("Response:", res.data)
        self.assertEqual(res.status_code, 401)

    def test_login_missing_email(self):
        print("\n======= Test: Missing Email =======\n")
        url = reverse("login")
        print("Sending only password")
        res = self.client.post(url, {"password": "adminpass"}, format="json")
        print("Response:", res.data)
        self.assertEqual(res.status_code, 401)

    def test_login_missing_password(self):
        print("\n======= Test: Missing Password =======\n")
        url = reverse("login")
        print("Sending only email")
        res = self.client.post(url, {"email": "admin@mail.com"}, format="json")
        print("Response:", res.data)
        self.assertEqual(res.status_code, 401)

    def test_login_empty_fields(self):
        print("\n======= Test: Empty Fields =======\n")
        url = reverse("login")
        print("Sending empty email and password")
        res = self.client.post(url, {"email": "", "password": ""}, format="json")
        print("Response:", res.data)
        self.assertEqual(res.status_code, 401)

    def test_login_nonexistent_user(self):
        print("\n======= Test: Non-existent User =======\n")
        res = self.login("ghost@mail.com", "somepass")
        print("Response:", res.data)
        self.assertEqual(res.status_code, 401)

    # -------- ONLY LOGGED-IN USER CAN VIEW THEIR GADGETS --------

    def test_unauthenticated_gadget_access(self):
        print("\n======= Test: Gadget Access Without Login =======\n")
        url = reverse("my-gadgets")
        res = self.client.get(url)
        print("Response Status:", res.status_code)
        self.assertEqual(res.status_code, 401)

    def test_user1_sees_only_their_own_gadgets(self):
        print("\n======= Test: User1 Gadget Visibility =======\n")
        login = self.login("u1@mail.com", "pass1")
        token = login.data["token"]

        print("Setting Authorization header...\n")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        url = reverse("my-gadgets")
        res = self.client.get(url)
        print("Gadget List:", res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], 2)

    def test_user2_sees_no_gadgets(self):
        print("\n======= Test: User2 Gadget Visibility (None) =======\n")
        login = self.login("u2@mail.com", "pass2")
        token = login.data["token"]

        print("Setting Authorization header...\n")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        url = reverse("my-gadgets")
        res = self.client.get(url)
        print("Gadget List:", res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], 0)
        self.assertEqual(len(res.data["items"]), 0)
    # -------- ONLY ADMIN CAN VIEW ALL GADGETS --------

    def test_admin_can_view_all_gadgets(self):
        print("\n======= Test: Admin Can View All Gadgets =======\n")

        # admin login
        login = self.login("admin@mail.com", "adminpass")
        print("Login Response:", login.data)

        token = login.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        url = reverse("admin-list")
        print("Requesting admin gadget list...\n")
        res = self.client.get(url)

        print("Admin Gadget List Response:", res.data)

        # EXPECTATION: Admin sees ALL gadgets from ALL users
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["total_items"], 2)
        self.assertEqual(len(res.data["items"]), 2)
        self.assertEqual(res.data["admin"], "admin")

    def test_normal_user_cannot_view_admin_list(self):
        print("\n======= Test: Normal User Forbidden From Admin List =======\n")

        # user1 logs in
        login = self.login("u1@mail.com", "pass1")
        print("Login Response:", login.data)

        token = login.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        url = reverse("admin-list")
        print("Requesting admin gadget list as NORMAL user...\n")
        res = self.client.get(url)

        print("Response:", res.data)

        self.assertEqual(res.status_code, 403)
        self.assertIn("msg", res.data)
        self.assertEqual(res.data["msg"], "Access Denied")

    def test_unauthenticated_user_cannot_access_admin_list(self):
        print("\n======= Test: Unauthenticated Access to Admin List =======\n")

        url = reverse("admin-list")
        print("Requesting admin gadget list WITHOUT login...\n")
        res = self.client.get(url)

        print("Response status:", res.status_code)

        self.assertEqual(res.status_code, 401)
