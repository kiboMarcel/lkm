from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Product
from base.serializers import ProductSerializer
from rest_framework import status


@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProductCategory(request):
    data = request.data
    products = Product.objects.filter(category=data['cat'])
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
  #  product = None
   # for i in Product:
    #    if i['_id'] == pk:
     #       product = i
      #      break
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)   