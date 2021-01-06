from django.shortcuts import render,get_object_or_404,redirect,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from App_Payment.models import Checkout
from App_Payment.forms import SaveAddressForm
from App_Order.models import Order,Cart
from django.contrib import messages
from django.urls import reverse_lazy,reverse


#Payment Gateway
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket
# import socket
from django.views.decorators.csrf import csrf_exempt
from django_xhtml2pdf.utils import generate_pdf
from django.http import HttpResponse
from django_xhtml2pdf.utils import pdf_decorator
# Create your views here.

@login_required
def CheckoutView(request):
    checkout_address=Checkout.objects.get_or_create(user=request.user)[0]
    val=checkout_address.fields_filled()
    print(val)
    form=SaveAddressForm(instance=checkout_address)
    if request.method=='POST':
        form=SaveAddressForm(request.POST,instance=checkout_address)
        if form.is_valid():
            form.save()
            form=SaveAddressForm(instance=checkout_address)
            messages.info(request, f"Shipping address successfully save!")
            return redirect('App_Payment:checkout')
    item=Order.objects.filter(user=request.user, ordered=False)
    item_list=item[0].orderitems.all()
    total=item[0].get_totals()
    print(item)
    return render(request, 'App_Payment/checkout.html', context={'form':form,'item':item_list,'total':total,'checkout_address':checkout_address})

@login_required
def PaymentGateWay(request):
    checkout_address=Checkout.objects.get_or_create(user=request.user)
    checkout_address=checkout_address[0]
    if not checkout_address.fields_filled():
        messages.info(request, f"Please complete shipping address!")
        return redirect("App_Payment:checkout")
    if not request.user.profile.get_filled():
        messages.info(request, f"Please complete profile details!")
        return redirect("App_Login:profile")

    sslc_store_id='googl5ff2ee6002050'
    sslc_store_pass='googl5ff2ee6002050@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=sslc_store_id, sslc_store_pass=sslc_store_pass)

    status_url=request.build_absolute_uri(reverse('App_Payment:complete'))
    failed=request.build_absolute_uri(reverse('App_Shop:home'))
    # print(status_url)

    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)
    
    order_item=Order.objects.filter(user=request.user, ordered=False)
    # order_item=order_item[0]
    item_all=order_item[0].orderitems.all()
    count_all=order_item[0].orderitems.count()
    total=order_item[0].get_totals()
    # print(item_all)
    # print(count_all)
    # print(total)

    

    mypayment.set_product_integration(total_amount=Decimal(total), currency='BDT', product_category='Mixed', product_name=item_all, num_of_item=count_all, shipping_method='Courier', product_profile='None')
    # mypayment.set_product_integration(total_amount=Decimal('200'), currency='BDT', product_category='Mixed', product_name='item_all', num_of_item=2, shipping_method='Courier', product_profile='None')

    current_user=request.user
    print(current_user.profile.city)
    mypayment.set_customer_info(name=current_user.profile.full_name, email=current_user.email, address1=current_user.profile.address_1, address2=current_user.profile.address_1, city=current_user.profile.city, postcode=current_user.profile.zipcode, country=current_user.profile.country, phone=current_user.profile.phone)

    mypayment.set_shipping_info(shipping_to=current_user.profile.full_name, address=checkout_address.address, city=checkout_address.city, postcode=checkout_address.zipcode, country=checkout_address.country)

    response_data = mypayment.init_payment()
    print(response_data)
    return redirect(response_data['GatewayPageURL'])

    # return render(request, 'App_Payment/payment.html', context={})

@csrf_exempt
# @login_required
def complete(request):
    if request.method=='POST' or request.method=='post':
        result=request.POST 
        print(result)
        tran_id=result['tran_id']
        val_id=result['val_id']
        status=result['status']
        tran_date=result['tran_date']
        amount=result['amount']
        card_type=result['card_type']

        if status=='VALID':
            messages.success(request,"Payment Successfull")
            return HttpResponseRedirect(reverse('App_Payment:purchas', kwargs={'tran_id':tran_id,'val_id':val_id,'tran_date':tran_date,'amount':amount,'card_type':card_type}))
        if status=='FAILED':
            messages.warning(request,"Payment Failed")
            return redirect('App_Shop:home')
        else:
            messages.warning(request,"Payment Failed")
            return redirect('App_Shop:home')
        
    return redirect('App_Shop:home')
    
@login_required
def purchas(request,tran_id,val_id,tran_date,amount,card_type):
    orders=Order.objects.filter(user=request.user, ordered=False)
    order=orders[0]
    if order:
        order.paymentId=tran_id
        order.orderId=val_id
        order.ordered=True
        order.save() 
        carts=Cart.objects.filter(user=request.user,purchased=False)
        for cart in carts:
            cart.purchased=True
            cart.save()
    else:
        return redirect('App_Shop:home')
    save_address=Checkout.objects.get(user=request.user)
    print(save_address)
    print(save_address.city)
    print(save_address.zipcode)
    return HttpResponseRedirect(reverse('App_Payment:receipt', kwargs={'tran_id':tran_id,'val_id':val_id,'tran_date':tran_date,'amount':amount,'card_type':card_type,'save_address':save_address}))
    
    
@login_required
def receipt(request,tran_id,val_id,tran_date,amount,card_type,save_address):
    
    return render(request, 'App_Payment/complete.html', context={'tran_id':tran_id,'val_id':val_id,'tran_date':tran_date,'amount':amount,'card_type':card_type,'save_address':save_address})
@pdf_decorator(pdfname='new_filename.pdf')
def pdfgenerate(request,tran_id,val_id,tran_date,amount,card_type,save_address):
    return render(request, 'App_Payment/complete.html', context={'tran_id':tran_id,'val_id':val_id,'tran_date':tran_date,'amount':amount,'card_type':card_type,'save_address':save_address})
