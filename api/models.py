from django.db import models

# Change Models Later with the boys
class Stock(models.Model):
    stockId = models.AutoField(primary_key=True)
    StockTicker = models.CharField(max_length=5)

class User(models.Model):
    userId = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=200)
    stocks = models.ManyToManyField(Stock,blank=True)
    money_spent = models.DecimalField(decimal_places=2, max_digits=11,null=True,blank=True) #max 1 billion with 2 0's

class UserStock(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.CharField(max_length=5)
    shares = models.IntegerField(null=True, blank=True)