# Generated by Django 4.0.3 on 2022-05-05 09:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_wallet_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Normal', 'Normal'), ('Warning', 'Warning'), ('Success', 'Success')], default='Normal', max_length=20)),
                ('title', models.CharField(blank=True, max_length=255)),
                ('body', models.CharField(blank=True, max_length=255)),
                ('visited', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]