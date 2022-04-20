from django.db import models


class PhotoGallery(models.Model):
    product = models.ForeignKey(to='product', related_name='gallery')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=400)


class Photo(models.Model):
    BUCKETS = (
        ('shops', 'shops'),
        ('site', 'site'),
        ('etc', 'etc')
    )
    photo = models.ImageField()
    alt_text = models.CharField(max_length=80)
    save_bucket = models.CharField()
    gallery = models.ForeignKey(to=PhotoGallery,
                                on_delete=models.CASCADE,
                                related_name='photos', null=True)
    
