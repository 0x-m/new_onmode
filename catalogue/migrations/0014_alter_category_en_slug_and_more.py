# Generated by Django 4.0.3 on 2022-04-24 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0013_productoptionvalue_delete_amodel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='en_slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_description',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_title',
            field=models.CharField(blank=True, max_length=90),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
