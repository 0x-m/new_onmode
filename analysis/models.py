from django.db import models

class Customer(models.Model):
    avatar = models.ForeignKey(to='Photo')
    

class Review(models.Model):
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(to='')
    body = models.TextField(blank=False, max_length=5000)
    published = models.BooleanField(default=False)
    rate = models.PositiveIntegerField(blank=True, null=True)

class Favourite(models.Model):
    pass    



class ProductStats(models.Model):
    product = models.OneToOneField(to='Product',
                                   on_delete=models.CASCADE,
                                   related_name='stats')
    views = models.IntegerField(default=0)
    reviews = models.IntegerField(default=0)
    sells = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    returns = models.IntegerField(default=0)
    rates = models.IntegerField(default=0)
    rates_avg = models.FloatField(default=0)
    
    def inc_views(self):
        self.views += 1
        self.save()

    def dec_views(self):
        if (self.views > 0):
            self.views -= 1
            self.save()

    def inc_reviews(self):
        self.reviews += 1
        self.save()

    def dec_reviews(self):
        if (self.reviews > 0):
            self.reviews -= 1
            self.save()

    def inc_likes(self):
        self.likes += 1
        self.save()

    def dec_likes(self):
        if (self.likes > 0):
            self.likes -= 1
            self.save()

    def inc_sells(self):
        self.sells += 1
        self.save()

    def dec_sells(self):
        if (self.sells > 0):
            self.sells -= 1
            self.save()
    
    def inc_returns(self):
        self.returns += 1
        self.save()
    
    def dec_returns(self):
        if (self.returns > 0):
            self.returns -= 1
            self.save()
    
    def inc_rates(self, rate):
        self.rates += 1
        self.save()
    
    def dec_rates(self):
        if (self.rates > 0):
            self.rates -= 1
            self.save()


class ShopStats(models.Model):
    shop = models.OneToOneField(to='Shop')
    no_products = models.PositiveIntegerField(default=0)
    no_views = models.PositiveIntegerField(default=0)
    no_customers = models.PositiveIntegerField(default=0)
    
    