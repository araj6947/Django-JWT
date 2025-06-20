from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, permissions
from .models import Book
from .serializers import BookSerializer
from .permission import IsWriterOrReadOnly

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsWriterOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)
