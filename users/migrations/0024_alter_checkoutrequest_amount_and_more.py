# Generated by Django 4.0.3 on 2022-05-16 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkoutrequest',
            name='amount',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='deposittransaction',
            name='amount',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='available',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='freezed',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]