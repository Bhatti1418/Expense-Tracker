from django.db import models

# Create your models here.
class Items(models.Model):
    name = models.CharField(max_length = 25,null=False)
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=0.0)
    total = models.DecimalField(max_digits=10,decimal_places=2,default=0)


    def __str__(self):
        return self.name

class Balance(models.Model):
    balance = models.FloatField(max_length=10, default=0)
    remaining_balance = models.FloatField(max_length=10, default=0)
    spend_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    count = models.FloatField(max_length=10, default=0)
    def __str__(self):
        return str(self.balance)

# class Client(models.Model):
#     name = models.CharField(max_length = 25,null=False)
#     balance = models.ForeignKey(Balance,on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name