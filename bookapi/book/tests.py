from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create users
        self.writer = User.objects.create_user(username="writer", password="writerpass")
        self.reader = User.objects.create_user(username="reader", password="readerpass")

        # Get JWT tokens
        self.writer_token = str(RefreshToken.for_user(self.writer).access_token)
        self.reader_token = str(RefreshToken.for_user(self.reader).access_token)

        # Create a book by writer
        self.book = Book.objects.create(title="Sample Book", description="Just a test", writer=self.writer)

        # Set up client
        self.client = APIClient()

    def test_1_get_books_unauthenticated(self):
        response = self.client.get("/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_2_get_book_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.reader_token}")
        response = self.client.get(f"/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Sample Book")

    def test_3_writer_can_create_book(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.writer_token}")
        data = {"title": "Writer's Book", "description": "By writer"}
        response = self.client.post("/books/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["writer"], self.writer.id)

    def test_4_reader_cannot_create_book(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.reader_token}")
        data = {"title": "Reader's Book", "description": "By reader"}
        response = self.client.post("/books/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_5_writer_can_update_own_book(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.writer_token}")
        response = self.client.put(f"/books/{self.book.id}/", {
            "title": "Updated Title",
            "description": "Updated",
            "writer": self.writer.id
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Title")

    def test_6_reader_cannot_update_others_book(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.reader_token}")
        response = self.client.put(f"/books/{self.book.id}/", {
            "title": "Hack",
            "description": "Trying to change",
            "writer": self.writer.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_7_writer_can_delete_own_book(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.writer_token}")
        response = self.client.delete(f"/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_8_reader_cannot_delete_book(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.reader_token}")
        response = self.client.delete(f"/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_9_get_books_authenticated_reader(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.reader_token}")
        response = self.client.get("/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_10_unauthenticated_cannot_create_book(self):
        response = self.client.post("/books/", {"title": "Book", "description": "No auth"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
