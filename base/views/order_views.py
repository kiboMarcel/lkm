from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from base.models  import Product, Order, OrderItem, ShippingAddress
from base.serializers import ProductSerializer, OrderSerializer

from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data

    print(data)
    orderItems = data['orderItems']

    if orderItems and len(orderItems) ==0:
        message = {'detail':'NO Orders Items  '}
        return Response(message, status= status.HTTP_400_BAD_REQUEST)

    else:
        # (1) Create Order
        order = Order.objects.create(
            user = user,
            paymentMethod=  data['paymentMethod'],
            taxPrice = data['taxPrice'],
            shippingPrice = data['shippingPrice'],
            totalPrice = data['totalPrice'],
        )

        # (2) create shipping address

        shipping = ShippingAddress.objects.create(
            order= order,
            address = data['shippingAddress']['address'],
            city = data['shippingAddress']['city'],
            postalCode = data['shippingAddress']['postalCode'],
            country = data['shippingAddress']['country']
        )

        # (3) create order items and set order to orderItem relationship
        for i in orderItems:
            product = Product.objects.get(_id=i['_id'])

            item = OrderItem.objects.create(
                product = product,
                order = order,
                name = product.name,
                qty = i['quantity'],
                price = i['price'],
                image = product.image.url,
            )    

            # (4) update stock

            product.countInStock -= item.qty
            product.save()

    serializer = OrderSerializer(order , many=False)
    return Response(serializer.data)

    """  data = request.data
        orderItems = data['orderItems']
        for i in orderItems:
            product = Product.objects.get(_id=i)

            return Response(product) """
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):

    user =  request.user

    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order , many= False)
            return Response(serializer.data)
        else:
            Response({'detail': 'Vous n\'etes pas authairizer a voir cette commande'},
            status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'La commande n\'existe pas '},
        status=status.HTTP_400_BAD_REQUEST)