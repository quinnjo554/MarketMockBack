from rest_framework.serializers import ModelSerializer
from .models import User, Stock


class Stock_Serializer(ModelSerializer):
    
    class Meta:
        model = Stock
        fields = '__all__'


class User_Serializer(ModelSerializer):
    stocks = Stock_Serializer(many=True)
    class Meta:
        model = User
        fields = '__all__'