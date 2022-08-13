# Generated by Django 4.0.3 on 2022-05-09 09:49

from django.db import migrations, models
import onmode.storage_backends


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0051_alter_collection_slug_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='index_poster',
            field=models.ImageField(blank=True, null=True, storage=onmode.storage_backends.SiteStorage(), upload_to=''),
        ),
        migrations.AlterField(
            model_name='collection',
            name='page_poster',
            field=models.ImageField(blank=True, null=True, storage=onmode.storage_backends.SiteStorage(), upload_to=''),
        ),
    ]
