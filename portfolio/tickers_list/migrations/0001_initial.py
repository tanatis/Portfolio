# Generated by Django 4.2.4 on 2023-08-17 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=5)),
                ('company_name', models.CharField(max_length=50)),
                ('index', models.CharField(choices=[('sp500', 'S&P 500'), ('dow', 'Dow Jones'), ('nasdaq', 'Nasdaq')], max_length=6)),
            ],
        ),
    ]
