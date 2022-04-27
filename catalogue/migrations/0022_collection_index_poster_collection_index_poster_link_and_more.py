# Generated by Django 4.0.3 on 2022-04-27 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0021_product_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='index_poster',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='collection',
            name='index_poster_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='index_view',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='collection',
            name='page_poster',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='collection',
            name='en_slug',
            field=models.SlugField(blank=True, editable=False),
        ),
        migrations.AlterField(
            model_name='collection',
            name='slug',
            field=models.SlugField(blank=True, editable=False),
        ),
    ]
