# Generated by Django 4.0.3 on 2022-05-08 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0030_contactusmessage_contactustype_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeoLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provinces', models.JSONField()),
                ('cities', models.JSONField()),
            ],
        ),
    ]
