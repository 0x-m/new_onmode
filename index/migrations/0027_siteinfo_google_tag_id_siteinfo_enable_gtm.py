# Generated by Django 4.0.3 on 2022-05-07 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0026_contactusmessages'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteinfo',
            name='GOOGLE_TAG_ID',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='siteinfo',
            name='enable_GTM',
            field=models.BooleanField(default=False),
        ),
    ]
