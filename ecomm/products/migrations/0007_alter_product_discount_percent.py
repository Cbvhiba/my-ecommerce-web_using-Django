# Generated by Django 3.2 on 2022-08-26 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20220826_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_percent',
            field=models.FloatField(default=0),
        ),
    ]
