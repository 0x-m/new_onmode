# Generated by Django 4.0.3 on 2022-05-09 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0048_remove_productstats_fails_remove_productstats_sales'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='en_slug',
            field=models.SlugField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='collection',
            name='slug',
            field=models.SlugField(blank=True, editable=False, null=True),
        ),
    ]
