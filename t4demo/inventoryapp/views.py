from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response



#Create your views here

from rest_framework.generics import ListAPIView
from .models import Product
from .serializer import ProductSerializer
from django.shortcuts import get_object_or_404

class ProductListCreateView(APIView):  # GET all, POST new item
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductUpdateView(APIView):  # PUT update by id
    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Item not found."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteView(APIView):  # DELETE by id
    def delete(self, request, pk):
        product = Product.objects.filter(pk=pk).first()
        if not product:
            return Response([], status=status.HTTP_204_NO_CONTENT)
        product.delete()
        return Response([], status=status.HTTP_204_NO_CONTENT)

class ProductCategoryQueryView(APIView):  # GET by category
    def get(self, request, category):
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductSortByPriceView(APIView):  # GET sorted by price descending
    def get(self, request):
        products = Product.objects.all().order_by('-price')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

