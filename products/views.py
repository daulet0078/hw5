import datetime
import random

from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
# Create your views here.
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.core.mail import send_mail


# Create your views here.


@api_view(['GET', 'POST'])
def products_list_view(request):
    if request.method == "POST":
        serializer = ProductCreateValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={
                'message': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price', 0)
        category = Category.objects.get(id=request.data.get('category'))
        product = Product.objects.create(title=title, description=description, price=price, category=category)
        product.tags.set(request.data['tags'])
        product.save()
        return Response(data={'message': "you posted new product!", "product": ProductListSerializer(product).data})
    products = Product.objects.all()
    data = ProductListSerializer(products, many=True).data
    return Response(data=data)


@api_view(['GET', 'PUT', 'DELETE'])
def products_item_view(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExistq:
        return Response(data={'message': "Product not Found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "DELETE":
        product.delete()
        return Response(data={"message": "Product is removed"})
    elif request.method == "PUT":
        serializer = ProductCreateValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={
                'message': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.tags.set(request.data['tags'])
        product.save()
        return Response(data={'message': 'Product updated', 'product': ProductListSerializer(product).data})
    data = ProductListSerializer(product).data
    return Response(data=data)


@api_view(['GET'])
def reviews_list_view(request):
    products = Product.objects.all()
    data = ProductsReviewListSerializer(products, many=True).data
    return Response(data=data)


@api_view(['GET'])
def active_tags_list_view(request):
    products = Product.objects.all()
    data = ProductsActiveTagsListSerializer(products, many=True).data
    return Response(data=data)


@api_view(['GET'])
def categories_list_view(request):
    category = Category.objects.all()
    data = CategoryListSerializer(category).data

    return data


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user:
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            return Response(data={
                'token': token.key
            })
        else:
            return Response(data={
                'message': "User not found"
            }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        code = str(random.randint(1000, 9999))
        user = User.objects.create_user(username=username, email=username, password=password, is_active=False)
        valid_until = datetime.datetime.now() + datetime.timedelta(minutes=60)
        ConfirmCode.objects.create(code=code, user=user, valid_until=valid_until)
        return Response(data={'message': 'User created'})

@api_view(['GET'])
def confirm(request, cd):

    code_list = ConfirmCode.objects.filter(code=cd, valid_until__gte=datetime.datetime.now())
    if code_list:
        confirmcode = code_list[0]
        confirmcode.user.is_active = True
        confirmcode.user.save()
        code_list.delete()
        return Response(data={'message': 'user activated'})
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
