from django.shortcuts import render
from .models import Item
from rest_framework import status
from .serializers import ItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class ItemListCreateView(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        barcode = request.data.get('barcode')
        if Item.objects.filter(barcode=barcode).exists():
            return Response("inventory with this barcode already exists", status=status.HTTP_400_BAD_REQUEST)
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response('', status=status.HTTP_400_BAD_REQUEST)

class ItemUpdateView(APIView):
    def put(self, request, pk):
        item = Item.objects.filter(pk=pk).first()
        if not item:
            return Response('',status=status.HTTP_400_BAD_REQUEST)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('', status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        item = Item.objects.filter(pk=pk).first()
        if item:
            item.delete()
            return Response('', status=status.HTTP_204_NO_CONTENT)
        return Response('', status=status.HTTP_400_BAD_REQUEST)

class ItemByCategory(APIView):
    def get(self,request,category):
        item = Item.objects.filter(category=category)
        if item:
            serializer = ItemSerializer(item, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('', status=status.HTTP_400_BAD_REQUEST)
    
class ItemSortByPrice(APIView):
    def get(self,request):
        '''item = Item.objects.all().order_by('-price')
        serializer = ItemSerializer(item, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)'''
        items = Item.objects.all().order_by('-price')
        if items:
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('', status=status.HTTP_400_BAD_REQUEST)