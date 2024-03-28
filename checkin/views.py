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

    # with open('/home/wondm/Desktop/dev/event-ticket-django/checkin/csvf.csv', 'r', encoding='utf-8') as file:
    #     reader = csv.DictReader(file)
    #     for row in reader:
    #         customer = Customer_2(
    #             ticket_id=row['ticket_id'],
    #             qr_value=row['qr_value'],
    #             # Default 'pending' if not provided

    #         )
    #         customer.save()


    if request.method == 'POST':
        val = request.POST.get('scanned_text')

        if val and len(val) > 10:
            try:
                customer = Customer.objects.filter(
                Q(nonce =val)  |
                Q(session_id=val)
            )
                
                return HttpResponse(customer)
            except Customer.DoesNotExist:
                return HttpResponse('notfound')
            
        elif len(val) == 8:
            try:
                customer2 = Customer_2.objects.filter(
                Q(qr_value =val) 
            ).first()
                
                return render(request, 'checkin/userform.html', {'user2': customer2})
            except Customer.DoesNotExist:
                return HttpResponse('notfound')



        else:
            return HttpResponse('nononce')
        
    else:
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
    return render(request, 'checkin/user.html', {'user': customer})


def update_customer_checkin2(request, customer_id):
    customer = Customer_2.objects.get(id=customer_id)  # Correct parameter here
    
    customer.check_in_status = 'SUCCESS'
    customer.save()
    return render(request, 'checkin/user2.html', {'user': customer})

def checkuser(request, user_id):
    userx = Customer.objects.get(id = user_id)
    return render(request, 'checkin/user.html', {'user' : userx})


def userform(request, user2_id):
    customer2 = Customer_2.objects.get(id=user2_id)
    if request.method == 'POST':
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        phone = request.POST.get('phone', None)
        email = request.POST.get('email', None)

        customer2.first_name = first_name
        customer2.last_name = last_name
        customer2.phone = phone
        customer2.email = email
        customer2.save()

        return render(request, 'checkin/user2.html', {'user' : customer2})
    else:
        return render(request, 'checkin/userform.html', {'customer2': customer2})