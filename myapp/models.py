from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class categories(models.Model):
    def __str__(self):
        return self.catname
    cat_id = models.IntegerField(primary_key = True)
    catname = models.CharField(max_length = 200)

class Item(models.Model):
    def __str__(self):
        return self.title
    category = models.ForeignKey(categories, on_delete=models.CASCADE)
    item_id = models.IntegerField(primary_key = True)
    title = models.CharField(max_length = 200)
    description = models.TextField(null=False)
    image_url = models.CharField(max_length = 200,null=True)
    rating = models.FloatField(default=0)
    price = models.IntegerField(default=0)

class Users(models.Model):
    def __str__(self):
        return self.name
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200)
    coins = models.IntegerField(default = 0)

class interaction(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

class checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.IntegerField(default = 1)

class orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.IntegerField(primary_key = True)

class orderdetails(models.Model):
    orders = models.ForeignKey(orders, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

class request(models.Model):
    itemname = models.CharField(max_length = 200)
    description = models.CharField(max_length = 200)

class productsrequests(models.Model):
    productname = models.CharField(max_length = 200)
    description = models.TextField(null=False)
