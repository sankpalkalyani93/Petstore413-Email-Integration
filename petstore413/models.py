from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pet(models.Model):
    name = models.CharField(max_length=255)
    age =  models.PositiveIntegerField()
    breed =  models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='pets/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}"
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    pet = models.ForeignKey(Pet, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}"

    def get_item_name(self):
        if self.pet:
            return self.pet.name
        return self.product.name
    
    @property
    def total(self):
        if self.product:
            return self.product.price * self.quantity
        if self.pet:
            return self.pet.price * self.quantity
        return 0