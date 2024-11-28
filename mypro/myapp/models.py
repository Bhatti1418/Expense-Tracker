from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add a ForeignKey to the User model
    name = models.CharField(max_length=25, null=True)

    def __str__(self):
        return self.name


class Items(models.Model):
    name = models.CharField(max_length = 25,null=False)
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=0.0)
    total = models.FloatField(max_length=10, default=0)
    catagory = models.CharField(max_length = 25,null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE,null = True)


    def __str__(self):
        return self.name


class Balance(models.Model):
    balance = models.FloatField(max_length=10, default=0)
    remaining_balance = models.FloatField(max_length=10, default=0)
    spend_amount = models.FloatField(max_length=10, default=0)
    count = models.FloatField(max_length=10, default=0)
    client = models.ForeignKey(Client,on_delete=models.CASCADE,null = True)
    def __str__(self):
        return str(self.balance)

