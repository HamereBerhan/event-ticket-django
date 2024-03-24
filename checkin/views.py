from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from ticketseller.models import Customer

from django.shortcuts import get_object_or_404
from django.db.models import Q
def scan_qr(request):
    return render(request, 'checkin/index.html')


def validate_user(request):
    if request.method == 'POST':
        nonce = request.POST.get('scanned_text')
        if nonce:
            try:
                # Query the Customer model to find a user with the given nonce
                customer = Customer.objects.get(nonce=nonce)
                # return JsonResponse({'status': 'success', 'customer_id': customer.id})
                return HttpResponse(customer)
            except Customer.DoesNotExist:
                # return JsonResponse({'status': 'error', 'message': 'User not found'})
                return HttpResponse('errro')
        else:
            # return JsonResponse({'status': 'error', 'message': 'Nonce value not provided'})
            return HttpResponse('errro')
        
    else:
        # Handle GET request (optional)
        # return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
        return HttpResponse('errro')



def search_customer(request):
    if request.method == 'POST':
        search_text = request.POST.get('search_text').strip()

        # Perform the search query
        if search_text == "":
            result_customer = None
        else:
            result_customer = Customer.objects.filter(
                Q(payment_status__icontains='SUCCESS')  & (
                Q(first_name__icontains=search_text) |
                Q(last_name__icontains=search_text) |
                Q(phone__icontains=search_text) |
                Q(email__icontains=search_text))
            ).first()
        return render(request, 'checkin/index.html', {'customer_find': result_customer})
    return render(request, 'checkin/index.html')


def update_customer_checkin(request, customer_id):
    customer = Customer.objects.get(id=customer_id)  # Correct parameter here
    
    customer.check_in_status = 'SUCCESS'
    customer.save()
    return redirect('home')
    return render(request, 'checkin/index.html', {'customer': customer})
