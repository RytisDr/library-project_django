# Generated by Django 3.0.4 on 2020-04-04 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog_app', '0004_magazine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magazine',
            name='summary',
            field=models.TextField(help_text='Enter a brief description of the magazine', max_length=1000),
        ),
    ]