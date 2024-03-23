from django.shortcuts import render

# Create your views here.

def scan_qr(request):
    return render(request, 'checkin/index.html')
