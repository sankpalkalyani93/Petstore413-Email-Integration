from django.db import models

# Create your models here.
class Pet(models.Model):
    name = models.CharField(max_length=255)
    age =  models.PositiveIntegerField()
    breed =  models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='pets/', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"