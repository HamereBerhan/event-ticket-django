from django.db import models

# Create your models here.

class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone  =models.CharField(max_length=15)
    email=models.EmailField(max_length=200)
    nonce =models.CharField(max_length=255)
    session_id=models.CharField(max_length=255)
    payment_status=models.CharField(max_length=255,default='pending')
    check_in_status= models.CharField(max_length=255,default='pending')
    created_at =models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name + ' ' +self.payment_status
class Customer_2(models.Model):
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    phone  =models.CharField(max_length=15, null=True)
    email=models.EmailField(max_length=200, null=True)
    ticket_id =models.CharField(max_length=255)
    qr_value=models.CharField(max_length=255)
    check_in_status= models.CharField(max_length=255,default='pending')
    created_at =models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now=True)

