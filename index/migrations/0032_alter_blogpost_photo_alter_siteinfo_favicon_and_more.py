# Generated by Django 4.0.3 on 2022-05-09 09:49

from django.db import migrations, models
import onmode.storage_backends


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0031_geolocation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='photo',
            field=models.ImageField(null=True, storage=onmode.storage_backends.SiteStorage(), upload_to=''),
        ),
        migrations.AlterField(
            model_name='siteinfo',
            name='favicon',
            field=models.ImageField(blank=True, null=True, storage=onmode.storage_backends.SiteStorage(), upload_to=''),
        ),
        migrations.AlterField(
            model_name='siteinfo',
            name='logo',
            field=models.ImageField(blank=True, null=True, storage=onmode.storage_backends.SiteStorage(), upload_to=''),
        ),
    ]