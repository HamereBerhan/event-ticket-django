from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from ticketseller.models import Customer, Customer_2

from django.shortcuts import get_object_or_404
from django.db.models import Q

import os
import csv
def scan_qr(request):
    return render(request, 'checkin/scanner.html')


def validate_user(request):

    with open('/home/wondm/Desktop/dev/event-ticket-django/checkin/csvf.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            customer = Customer_2(
                ticket_id=row['ticket_id'],
                qr_value=row['qr_value'],
                # Default 'pending' if not provided

            )
            customer.save()


    if request.method == 'POST':
        val = request.POST.get('scanned_text')

        if val and len(val) > 10:
            try:
                # Query the Customer model to find a user with the given nonce
                # customer = Customer.objects.filter(nonce=val)
                customer = Customer.objects.filter(
                Q(nonce =val)  |
                Q(session_id=val)
            )
                
                # return JsonResponse({'status': 'success', 'customer_id': customer.id})
                return HttpResponse(customer)
            except Customer.DoesNotExist:
                # return JsonResponse({'status': 'error', 'message': 'User not found'})
                return HttpResponse('notfound')


        else:
            # return JsonResponse({'status': 'error', 'message': 'Nonce value not provided'})
            return HttpResponse('nononce')
        
    else:
        # Handle GET request (optional)
        # return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
        return HttpResponse('errro')



def search_customer(request):
    if request.method == 'POST':
        print(1)
        search_text = request.POST.get('search_text').strip()

        # Perform the search query
        if search_text == "":
            result_customer = None
            print(2)
        else:
            print(3)
            result_customer = Customer.objects.filter(
                Q(payment_status__icontains='SUCCESS')  & (
                Q(first_name__icontains=search_text) |
                Q(last_name__icontains=search_text) |
                Q(phone__icontains=search_text) |
                Q(email__icontains=search_text))
            )
        return render(request, 'checkin/search.html', {'customer_find': result_customer})
    return render(request, 'checkin/search.html')


def update_customer_checkin(request, customer_id):
    customer = Customer.objects.get(id=customer_id)  # Correct parameter here
    
    customer.check_in_status = 'SUCCESS'
    customer.save()
    return redirect('home')
    return render(request, 'checkin/index.html', {'customer': customer})
