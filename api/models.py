from django.db import models

# Change Models Later with the boys
class Stock(models.Model):
    stockId = models.AutoField(primary_key=True)
    StockTicker = models.CharField(max_length=5)


class User(models.Model):
    userId = models.AutoField(primary_key=True)
    stocks = models.ManyToManyField(Stock)
    money_current = models.DecimalField(decimal_places=2, max_digits=11) #max 1 billion with 2 0's


