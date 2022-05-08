# Generated by Django 4.0.3 on 2022-05-07 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='custom_storage_capacity',
            field=models.FloatField(default=20, help_text='custom storage in mega bytes'),
        ),
        migrations.AddField(
            model_name='user',
            name='use_custom_storage_capcity',
            field=models.BooleanField(default=False, help_text='check if you want arbitrary storage capacity for this user'),
        ),
        migrations.AlterField(
            model_name='user',
            name='consumed_storage',
            field=models.FloatField(default=0, help_text='consumed storage in mega bytes'),
        ),
    ]