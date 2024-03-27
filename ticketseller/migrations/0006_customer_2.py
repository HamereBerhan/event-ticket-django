# Generated by Django 4.2.7 on 2024-03-27 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketseller', '0005_alter_customer_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer_2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('email', models.EmailField(max_length=200, null=True)),
                ('ticket_id', models.CharField(max_length=255)),
                ('qr_value', models.CharField(max_length=255)),
                ('check_in_status', models.CharField(default='pending', max_length=255)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]