# Generated by Django 3.1.5 on 2021-01-28 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lookup_hub', '0011_auto_20210128_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='order',
            field=models.FloatField(),
        ),
    ]
