# Generated by Django 4.2.4 on 2023-08-17 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks_portfolio', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='position',
        ),
        migrations.DeleteModel(
            name='Position',
        ),
    ]
