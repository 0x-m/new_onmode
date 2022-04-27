# Generated by Django 4.0.3 on 2022-04-27 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0011_mainstack_about_mainstack_laws'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='collection',
        ),
        migrations.RemoveField(
            model_name='sliderphoto',
            name='slider',
        ),
        migrations.AddField(
            model_name='sliderphoto',
            name='precedence',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='MainStack',
        ),
        migrations.DeleteModel(
            name='Section',
        ),
        migrations.DeleteModel(
            name='Slider',
        ),
    ]