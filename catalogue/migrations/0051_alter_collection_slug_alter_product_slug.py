# Generated by Django 4.0.3 on 2022-05-09 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0050_alter_category_en_slug_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, null=True),
        ),
    ]
