# Generated by Django 4.0.3 on 2022-04-25 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_user_consumed_storage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='consumed_storage',
            field=models.FloatField(default=0),
        ),
    ]
