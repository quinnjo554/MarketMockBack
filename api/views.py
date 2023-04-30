from django.shortcuts import render
from rest_framework.response import Response

from rest_framework import status
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

@api_view(['GET'])
def getUserByEmail(request,pk):
      users = User.objects.get(userName = pk)
      serializer = User_Serializer(users, many=False)
      return Response(serializer.data)


@api_view(['GET'])
def getStock(request):
      stock = Stock.objects.all()
      serializer = Stock_Serializer(stock, many=True)
      return Response(serializer.data)

@api_view(['POST'])
def create_user(request):
    username = request.data.get('userName')
    if User.objects.filter(userName=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = User_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_stocks(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    ticker = request.data.get('StockTicker')
    shares = request.data.get('shares')
    if Stock.objects.filter(StockTicker=ticker).exists():
        id = Stock.objects.get(StockTicker=ticker)
        return Response({"stockId":id.stockId }) #Add update Stock function
    if not shares:
         return Response({'error': 'Shares not provided.'}, status=status.HTTP_400_BAD_REQUEST)
    if shares <= 0 :
          return Response({'error': 'Invaild stock amount'}, status=status.HTTP_400_BAD_REQUEST)

    if not ticker:
        return Response({'error': 'Ticker symbol not provided.'}, status=status.HTTP_400_BAD_REQUEST)
    
    stock = Stock.objects.create(StockTicker=ticker, shares=shares)
    user.stocks.add(stock)
    user.save()
    
    return Response({
        'success': f'Stock {ticker} added to user {pk} with {shares} number of shares.',
        'stockId': stock.stockId
    }, status=status.HTTP_201_CREATED)



@api_view(['POST'])
def sell_shares(request, u_pk, s_pk):
    try:
        user = User.objects.get(pk=u_pk)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        stock = Stock.objects.get(pk=s_pk)
    except Stock.DoesNotExist:
        return Response({'message': 'Stock not found'}, status=status.HTTP_404_NOT_FOUND)

    shares = request.data.get('shares')

    if shares is None:
        return Response({'message': 'Shares not provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        shares = int(shares)
    except ValueError:
        return Response({'message': 'Invalid shares value'}, status=status.HTTP_400_BAD_REQUEST)

    if shares <= 0:
        return Response({'message': 'Shares must be greater than zero'}, status=status.HTTP_400_BAD_REQUEST)

    
    return Response({'message': 'Shares sold successfully'}, status=status.HTTP_200_OK)