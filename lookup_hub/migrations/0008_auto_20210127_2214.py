# Generated by Django 3.1.5 on 2021-01-27 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lookup_hub', '0007_auto_20210127_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictionary',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
