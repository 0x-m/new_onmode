# Generated by Django 4.0.3 on 2022-04-26 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0007_aboutsite_laws_slider_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainstack',
            name='about',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='index.aboutsite'),
        ),
        migrations.AddField(
            model_name='mainstack',
            name='laws',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='index.laws'),
        ),
    ]
