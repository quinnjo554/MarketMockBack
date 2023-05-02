from rest_framework.serializers import ModelSerializer
from .models import User, Stock,UserStock


class Stock_Serializer(ModelSerializer):
    
    class Meta:
        model = Stock
        fields = '__all__'


class User_Serializer(ModelSerializer):
    stocks = Stock_Serializer(many=True,read_only=True)
    class Meta:
        model = User
        fields = '__all__'

class UserStock_Serializer(ModelSerializer):
    class Meta:
        model = UserStock
        fields = '__all__'