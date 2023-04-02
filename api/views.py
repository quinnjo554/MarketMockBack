from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User,Stock
from .serializers import User_Serializer, Stock_Serializer

# Create your views here.
#install Django rest framwork with python -m install djangorestframework
@api_view(['GET'])
def getRoutes(request):
      routes = [
        {
        'Endpoint': '/User/',
        'method': 'GET',
        'body': None,
        'description': 'returns a list of Users'
        },  
        {
        'Endpoint': '/Stock/create/',
        'method': 'POST',
        'body': {'body':""},
        'description': 'Creates a Stock with data sent'
        }

    ]   
      return Response(routes)


@api_view(['GET'])
def getUsers(request):
      users = User.objects.all()
      serializer = User_Serializer(users, many=True)
      return Response(serializer.data)

#Only returns the number of stocks the user has not the id or ticker fix later
@api_view(['GET'])
def getUser(request,pk):
      users = User.objects.get(userId = pk)
      serializer = User_Serializer(users, many=False)
      return Response(serializer.data)

