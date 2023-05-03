from decimal import Decimal
from django.shortcuts import render
from rest_framework.response import Response

from rest_framework import status
from rest_framework.decorators import api_view
from .models import User,Stock, UserStock
from .serializers import User_Serializer, Stock_Serializer, UserStock_Serializer

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

@api_view(['DELETE'])
def userStockDelete(request, user_id, stock_id):
    try:
        userstock = UserStock.objects.get(user=user_id, stock=stock_id)
    except UserStock.DoesNotExist:
        return Response({'message': 'UserStock does not exist'}, status=status.HTTP_404_NOT_FOUND)

    userstock.delete()
    return Response({'message': 'UserStock deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

#Gets all the users 
@api_view(['GET'])
def getUsers(request):
      users = User.objects.all()
      serializer = User_Serializer(users, many=True)
      return Response(serializer.data)




#returns all a users data use to get money spent
@api_view(['GET'])
def getUser(request,pk):
      users = User.objects.get(userId = pk)
      serializer = User_Serializer(users, many=False)
      return Response(serializer.data)

#Updates a specific users money_spent
@api_view(['PUT'])
def updateUserMoneySpent(request, pk, money):
    try:
        user = User.objects.get(userId=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.money_spent is None:
        user.money_spent = Decimal('0')
    user.money_spent += Decimal(money)
    user.save()
    return Response({'message': 'User money spent updated successfully'})


#gets all the info for a user with the email
@api_view(['GET'])
def getUserByEmail(request,pk):
      users = User.objects.get(userName = pk)
      serializer = User_Serializer(users, many=False)
      return Response(serializer.data)


#gets all the stocks associated to a user
@api_view(['GET'])
def getUserStocks(request, u_id):
    userStocks = UserStock.objects.filter(user=u_id)
    serializer = UserStock_Serializer(userStocks, many=True)
    return Response(serializer.data)


#gets all the stock objects
@api_view(['GET'])
def getStock(request):
      stock = Stock.objects.all()
      serializer = Stock_Serializer(stock, many=True)
      return Response(serializer.data)

##
## Update User stocks 
## get the pk and sk from request body
## Its Put because its modifing a row that already exist
@api_view(['PUT'])
def UpdateUserStockBuy(request, user_id, stock_ticker, shares):
    try:
        user_stock = UserStock.objects.get(user_id=user_id, stock=stock_ticker)
    except UserStock.DoesNotExist:
        return Response("User stock does not exist")

    # Update the shares field of the UserStock object
    user_stock.shares += int(shares)
    user_stock.save()

    return Response(f"User {user_stock.user.userName} updated shares of {user_stock.stock} to {user_stock.shares}")

@api_view(['PUT'])
def UpdateUserStockSell(request, user_id, stock_ticker, shares):
    try:
        user_stock = UserStock.objects.get(user_id=user_id, stock=stock_ticker)
    except UserStock.DoesNotExist:
        return Response("User stock does not exist")

    # Check if user has enough shares to sell
    if user_stock.shares < int(shares):
        return Response(f"User {user_stock.user.userName} does not have enough shares to sell")

    # Update the shares field of the UserStock object
    user_stock.shares -= int(shares)
    user_stock.save()

    return Response(f"User {user_stock.user.userName} updated shares of {user_stock.stock} to {user_stock.shares}")


@api_view(['POST'])
def create_Stock(request, stock_ticker):
    # Try to retrieve the stock from the database
    stock, created = Stock.objects.get_or_create(StockTicker=stock_ticker)

    # If the stock already exists, return its ID
    if not created:
        return Response({'success': True, 'stock': {'id': stock.stockId}})

    # Otherwise, save the new stock object and return its details
    stock.save()
    return Response({'success': True, 'stock': {'id': stock.stockId, 'StockTicker': stock.StockTicker}})
# 
# Run Create Stock First
# In THe stock Landing
# 
@api_view(['POST'])
def addStockToUser(request, u_id, ticker, shares):
    try:
        user = User.objects.get(userId=u_id)
        stock = Stock.objects.get(StockTicker=ticker)
    except (User.DoesNotExist, Stock.DoesNotExist):
        return Response("User or stock gone")

    if UserStock.objects.filter(user=user).count() >= 5:
        return Response({"message":f"User {user.userName} already has 5 stocks."})
    elif UserStock.objects.filter(user=user, stock=stock.StockTicker).exists():
        return Response({"message":f"User {user.userName} already has {stock.StockTicker}"})
    else:
        user_stock = UserStock.objects.create(user=user, stock=stock.StockTicker, shares=shares)
        user_stock.save()
    return Response({"message": f"User {user.userName} added {shares} shares of {stock.StockTicker}"})


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

