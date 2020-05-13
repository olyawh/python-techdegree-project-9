from django.db import models
from django.utils import timezone


class Menu(models.Model):
    '''Menu model'''    
    season = models.CharField(max_length=255)
    items = models.ManyToManyField('Item', related_name='items')
    created_date = models.DateTimeField(
            default=timezone.now)
    expiration_date = models.DateTimeField(
            blank=True, null=True)

    def __str__(self):
        return self.season

class Item(models.Model):
    '''Item model'''    
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    chef = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_date = models.DateTimeField(
            default=timezone.now)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    '''Ingredient model'''    
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
