# Generated by Django 4.0.3 on 2022-05-05 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0023_certificate'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='show_on_index',
            field=models.BooleanField(default=False),
        ),
    ]