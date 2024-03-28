"""
URL configuration for ticket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static


import ticketseller.views as handlers
import checkin.views as checkin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buy/',handlers.buy_ticket),
    path('ticket/<str:nonce>',handlers.generateTicket),
    path('notify/',handlers.notify),
    path('success/<str:nonce>',handlers.success),
    path('err/', handlers.error),
    path('', handlers.home, name='home'),
    path('scancode/', checkin.scan_qr, name='scan'),
    path('validate/', checkin.validate_user ,name = 'validator'),
    path('search/', checkin.search_customer, name='search'),
    path('checkin/<int:customer_id>', checkin.update_customer_checkin, name='update'),
    path('checkuser/<int:user_id>', checkin.checkuser, name='user'),
    path('userform/<int:user2_id>', checkin.userform, name='userform'),
    path('checkin2/<int:customer_id>', checkin.update_customer_checkin2, name='update2'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
