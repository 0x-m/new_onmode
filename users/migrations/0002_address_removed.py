# Generated by Django 4.0.3 on 2022-04-22 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='removed',
            field=models.BooleanField(default=False),
        ),
    ]