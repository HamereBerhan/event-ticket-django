# Generated by Django 5.0.2 on 2024-02-29 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketseller', '0004_alter_customer_nonce'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=200),
        ),
    ]
