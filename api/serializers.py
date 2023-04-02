from rest_framework.serializers import ModelSerializer
from .models import User, Stock

class User_Serializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class Stock_Serializer(ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'
