# Generated by Django 4.0.3 on 2022-04-23 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0009_rename_status_createshoprequest_reject_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('options', models.ManyToManyField(related_name='types', to='catalogue.option')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='catalogue.producttype'),
        ),
    ]
