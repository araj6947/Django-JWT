from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from rest_framework.generics import CreateAPIView
from .serializers import ItemSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.

class RegisterView(CreateAPIView):
    serializer_class = UserSerializer

class CheckAuthView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({"message": "✅ You are authenticated!", "user": request.user.username})
        else:
            return Response({"message": "❌ You are NOT authenticated!"}, status=401)

class ItemListCreateView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        barcode = request.data.get('barcode')
        if Item.objects.filter(barcode=barcode).exists():
            return Response("inventory with this barcode already exists", status=status.HTTP_400_BAD_REQUEST)
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        item = Item.objects.filter(pk=pk).first()
        if not item:
            return Response({"error": "Item not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        item = Item.objects.filter(pk=pk).first()
        if item:
            item.delete()
            return Response([], status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Item not found"}, status=status.HTTP_400_BAD_REQUEST)

class ItemByCategory(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, category):
        items = Item.objects.filter(category=category)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ItemSortByPrice(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        items = Item.objects.all().order_by('-price')
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)