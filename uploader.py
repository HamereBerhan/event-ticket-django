import os
import csv
import django
from datetime import datetime
from ticketseller.models import Customer_2

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticket.settings')
django.setup()

def import_data_from_csv(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            customer = Customer_2(
                ticket_id=row['ticket_id'],
                qr_value=row['qr_value'],
                check_in_status=row['check_in_status'] if 'check_in_status' in row else 'pending',  # Default 'pending' if not provided
# Default to current time
            )
            customer.save()

# if name == "main":
#     csv_file_path = 'csvf.csv'
#     import_data_from_csv(csv_file_path)