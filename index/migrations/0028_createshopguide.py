# Generated by Django 4.0.3 on 2022-05-07 06:03

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0027_siteinfo_google_tag_id_siteinfo_enable_gtm'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreateShopGuide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', tinymce.models.HTMLField()),
            ],
        ),
    ]