# Generated by Django 4.0.3 on 2022-05-01 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0003_giftcard_code_giftcard_end_date_giftcard_start_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftcard',
            name='date_used',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]
