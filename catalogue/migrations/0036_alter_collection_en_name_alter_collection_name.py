# Generated by Django 4.0.3 on 2022-04-30 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0035_alter_product_sales_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='en_name',
            field=models.CharField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='collection',
            name='name',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]
