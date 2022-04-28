from email.policy import default
from nis import cat
from shutil import ExecError
from django.db import models
from users.models import User
from catalogue.models import Collection, Product, Shop
from promotions.models import Coupon

class Cart(models.Model):
    user = models.ForeignKey(
        to=User, related_name='carts', on_delete=models.CASCADE)
    shop = models.ForeignKey(
        to=Shop, related_name='carts', on_delete=models.CASCADE)
    coupon = models.ForeignKey(
        to=Coupon, related_name='cart', on_delete=models.SET_NULL, null=True)
    final_price = models.PositiveBigIntegerField(default=0)

    def __len__(self):
        return len(self.items.all())

    def __str__(self) -> str:
        return self.shop.name

    @property
    def quantity(self):
        return len(self)

    @property
    def total(self):
        '''
        total price before applying coupon
        '''
        total = 0
        for item in self.items.all():
            total += item.total
        return total

    @property
    def final_price(self):
        '''
        total price after applying coupon
        '''
        total = self.total
        coupon = self.coupon
        if coupon:
            pass

        return total

    def is_valid(self):
        for item in self.items.all():
            if not item.is_valid():
                return False
            return True

    def update(self):
        for item in self.items.all():
            item.update()

    def checkout(self):
        pass


class CartItem(models.Model):
    product = models.ForeignKey(
        to=Product, related_name='incart', on_delete=models.CASCADE)
    collection = models.ForeignKey(to=Collection, related_name='cartitems', on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(
        to=Cart, related_name='items', on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    options = models.JSONField(null=True)

    def update(self):
        self.price = self.product.compute_price(self.collection)
        self.save()

    def is_valid(self):
        return self.price == self.product.compute_price(self.collection) and self.product.has_quantity(self.quantity)

    @property
    def total(self):
        return self.quantity * self.price

    def increment(self):
        if self.product.has_qunatity(self.quantity + 1):
            self.quantity += 1
            self.save()

    def decrement(self):
        if self.quantity > 0:
            self.quantity -= 1
            self.save()
        if self.quantity == 0:
            # TODO: create a new exceptio derived class...
            raise Exception('this item must be deleted')
