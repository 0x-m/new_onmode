# Generated by Django 4.0.3 on 2022-05-01 18:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('promotions', '0004_alter_giftcard_date_used'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftcard',
            name='user',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gifts', to=settings.AUTH_USER_MODEL),
        ),
    ]
