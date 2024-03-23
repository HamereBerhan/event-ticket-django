from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO
import json
import smtplib
import uuid
from django.shortcuts import render,redirect
from ticket.settings import PAYMENT_SETTINGS,EMAIL_SETTINGS,SMS_SETTINGS
import django.core.exceptions as exec
from datetime import datetime, timedelta
import requests
from django.http import FileResponse, HttpResponse, HttpResponseBadRequest
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import os
import qrcode
from .models import Customer
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
def buy_ticket(request):
   

    if request.method == 'POST':
        
        first_name = request.POST.get('first_name','').encode('utf-8').decode('utf-8')
        last_name= request.POST.get('last_name','').encode('utf-8').decode('utf-8')
        email = request.POST['email']
        phone=request.POST['phone']
        current_time = datetime.now()
        new_time = current_time + timedelta(hours=PAYMENT_SETTINGS["DURATION"])
        exdate = new_time.strftime("%Y-%m-%dT%H:%M:%S")
        # unique value uuid for nonce
        nonce = uuid.uuid4()
        if len(phone) < 9 or not (phone[-9]=='9' or phone[-9]=='7' ):
            return HttpResponse(content='invalid phone number', status=400)
        elif len(phone) > 9:
            phone = '251' + phone[-9:]
        else:
            phone='251'+phone
        #  Your request payload (data to be sent)
        data = {
            "cancelUrl": PAYMENT_SETTINGS['CANCEL_URL'],
            "nonce": str(nonce),
            "phone": phone,
            "email": email,
            "errorUrl": PAYMENT_SETTINGS['ERROR_URL'],
            "notifyUrl": PAYMENT_SETTINGS['NOTIFY_URL'],
            "successUrl": PAYMENT_SETTINGS['SUCCESS_URL']+'/'+str(nonce),
            "paymentMethods": [
                "TELEBIRR"
            ],
            "expireDate": exdate,
            "items": [
                {
                    "description": " ንጹሕ ምንጭ ኢትዮጵያ ልዩ ዓውደ ርእይ መግቢያ ትኬት",
                    "image": "https://hamereberhan.org/web%20ticket%20square%20image-01-01N.webp",
                    "name": "የመግቢያ ትኬት",
                    "price": PAYMENT_SETTINGS['ITEM_PRICE'],
                    "quantity": 1
                },
            ],
            "beneficiaries": [
                {
                    "accountNumber": PAYMENT_SETTINGS['ACCOUNT_NUMBER'],
                    "bank": PAYMENT_SETTINGS['BANK'],
                    "amount": PAYMENT_SETTINGS['AMOUNT']
                }
            ],
            "lang": "EN"
        }
    
    
        headers={
        "Content-Type":"application/json",
        "x-arifpay-key": PAYMENT_SETTINGS['API_KEY']
        }
        res=requests.post(url=PAYMENT_SETTINGS['SESSION_URL'],json=data,headers=headers)
        # res= arifpay.Make_payment(paymentInfo)
    
        data= res.json()
        if res.status_code!=200:
            raise exec.BadRequest('failed to create checkout session')
    
        # register customer to database
        registeruser(first_name,last_name,phone,email,nonce,data['data']['sessionId'],'pending','pending')
        return redirect(data['data']['paymentUrl']) 
    else:
        # Handle GET requests or other methods
        return HttpResponse("bad request",status=400)
   
    
def home(request):

    return render(request, 'ticketseller/home.html')

def success(request,nonce):
    return render(request,'ticketseller/success.html')
    
def error(request):
    return HttpResponse("Some thing went wrong !")

def generateTicket(request,nonce):
    user=Customer.objects.get(nonce=nonce)
    
    height = 7.5 *cm
    width = 20*cm
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawImage('./static/image/Tiket_BG-01-01.png',0,22*cm,width, height)
    img= gen_qrcode(user.session_id)
    c.drawInlineImage(img,16*cm,25*cm)
     #c.drawString(16*cm,22.8*cm,'Name:'+ user.first_name + user.last_name)
     #c.drawString(16.5*cm,22.4*cm,'Phone:'+user.phone)
    c.drawString(17.5*cm,22.4*cm, 'E' + '0'*(5 -len(str(user.id))) + str(user.id))
    c.showPage()
    c.save()

    # Seek back to the beginning of the buffer before reading
    buffer.seek(0)

    # Create a FileResponse and serve the PDF
    newbuf=ContentFile(buffer.getvalue(), name='ticket.pdf')
    response = HttpResponse(newbuf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ticket.pdf"'
    return response
  

@csrf_exempt
def notify(request):
    if request.method == 'POST':
            try:
                json_data = json.loads(request.body.decode('utf-8'))
                print("JSON Data:", json_data)
                    
                if json_data['transactionStatus']=='SUCCESS':  
                    # update payment status
                    user=updatePaymentstatus(session_id=json_data['sessionId'],status='SUCCESS')            
                    gen_pdf('./static/image/Tiket_BG-01-01.png','./static/pdf/',user)
                        
                    # send message 
                    send_sms(user)
                    # send email
                    send_email(user,'./static/pdf/'+ str(user.nonce)+'.pdf')
                    return HttpResponse(content='done', content_type='application/json', status=200)
                    
            except json.JSONDecodeError:
                    print('send bad request so that callback will be called again ')
                    return HttpResponseBadRequest(status=400)
    else:
                # Handle GET requests or other methods
        return HttpResponse(status=400)
        
    

def gen_pdf(image_path,output_pdf,user):
    
    img= gen_qrcode(user.nonce)

    height = 7.5 *cm
    width = 20*cm
    c = canvas.Canvas(output_pdf+str(user.nonce)+'.pdf')
    # for image_path in image_path: './static/qr/'+str(user.nonce)+'.png'
    c.drawImage(image_path,0,22*cm,width, height)
    c.drawInlineImage(img,16*cm,25*cm)
     #c.drawString(16*cm,22.8*cm,'Name:'+ user.first_name + user.last_name)
     #c.drawString(16.5*cm,22.4*cm,'Phone:'+user.phone)
    c.drawString(17.5*cm,22.4*cm, 'E' + '0'*(5 -len(str(user.id))) + str(user.id))
    c.showPage()
    c.save()

    return

# qr generator
def gen_qrcode(nonce):
    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=2,
        )
    qr.add_data(nonce)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white") 
    # img.save('./static/qr/'+str(nonce)+'.png') 
    return img

def registeruser(first_name,last_name,phone,email,nonce,session_id,payment_status,check_in_status):
    customer=Customer(
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        email=email,
        nonce=nonce,
        session_id=session_id,
        payment_status=payment_status,
        check_in_status=check_in_status,
        )
    customer.save()

def updatePaymentstatus(session_id,status):
    customer=Customer.objects.get(session_id=session_id)
    customer.payment_status=status
    customer.updated_at=datetime.now()
    customer.save()
    return customer



# send email to customer
def send_email(user, attachment_path=None):
    email_host = EMAIL_SETTINGS['HOST']
    email_port = 587
    email_user = EMAIL_SETTINGS['USER_NAME']
    email_password = EMAIL_SETTINGS['PASSWORD']
    
    message=f'''ውድ {user.first_name} ከሐመረ ብርሃን በግዮን ሆቴል ለሚካሔደው የ"ንጹሕ ምንጭ ኢትዮጵያ" ልዩ ዓውደ ርእይ የመግቢያ ካርድ ገዝተዋል።
     የቲኬት ቁጥር፡- {'E' + '0'*(5 -len(str(user.id))) + str(user.id)}
     ቦታ፦ ግዮን ሆቴል
     ቀን፡ ሚያዝያ 5 -13 2016 ዓ.ም
     '''
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SETTINGS['USER_NAME']
    msg['To'] = user.email
    msg['Subject'] = EMAIL_SETTINGS['SUBJECT']

    msg.attach(MIMEText(message, 'plain'))

    if attachment_path:
        attachment = MIMEBase('application', 'octet-stream')
        with open(attachment_path, 'rb') as file:
            attachment.set_payload(file.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
        msg.attach(attachment)

    try:
        server = smtplib.SMTP(email_host, email_port)
        server.starttls()
        server.login(email_user, email_password)
        server.send_message(msg)
        print('Email sent successfully!')

    except Exception as e:
        print('An error occurred while sending the email:', str(e))

    finally:
        server.quit()
        
        
# send sms to customer
def send_sms(user):
    api_token = SMS_SETTINGS['TOKEN']
    message = f'''
         ውድ {user.first_name} ከሐመረ ብርሃን በግዮን ሆቴል ለሚካሔደው የንጹሕ ምንጭ ኢትዮጵያ - ልዩ ዓውደ ርእይ የመግቢያ ካርድ ገዝተዋል።
         የቲኬት ቁጥር፡- {'E' + '0'*(5 -len(str(user.id))) + str(user.id)}
        '''
    api_url = SMS_SETTINGS['URL']

    payload = {
        "token": api_token,
        "phone": user.phone,
        "msg": message,
    }
    response = requests.post(api_url, json=payload)
    if response.status_code!=200:
        return HttpResponseBadRequest
    print("sms sent successfully")
    return response
