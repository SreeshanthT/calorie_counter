from django.db import models

# Create your models here.

class FoodItems(models.Model):
    food = models.CharField("Food Item",max_length=100,null=True)
    caloire = models.IntegerField("Calories")
