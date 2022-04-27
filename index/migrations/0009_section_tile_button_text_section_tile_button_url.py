# Generated by Django 4.0.3 on 2022-04-26 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0008_mainstack_about_mainstack_laws'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='tile_button_text',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='section',
            name='tile_button_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]