from django.shortcuts import render,get_object_or_404,redirect,HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse
from App_Order.models import Cart,Order 
from App_Shop.models import Product
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from App_Login.models import User
# Create your views here.
from django.contrib.auth.decorators import login_required
# from App_Order.models import Order,Cart

def add_to_cart(request,pk):
    item=get_object_or_404(Product,pk=pk)
    cart_item=Cart.objects.get_or_create(user=request.user,item=item,purchased=False)
    # print(cart_item)
    # print(cart_item)
    ordered_item=Order.objects.filter(user=request.user,ordered=False)
    if ordered_item.exists():
        # print("True")
        order=ordered_item[0]
        if order.orderitems.filter(item=item).exists():
            cart_item[0].quantity +=1
            cart_item[0].save()
            messages.info(request, "This item quantity was updated.")
            # messages.info(request, "email send")
            return redirect('App_Shop:home')
        else:
            order.orderitems.add(cart_item[0])
            # order.save()
            messages.info(request, "This item was added to your cart.")
            return redirect("App_Shop:home")
    else:
        print("new Ordered created")
        order=Order(user=request.user)
        order.save()
        order.orderitems.add(cart_item[0])
        messages.info(request, "This item was added to your cart.")
        return redirect('App_Shop:home')
    # return HttpResponseRedirect(reverse('App_Shop:home', ))
    
    
@login_required
def cart_template(request):
    carts=Cart.objects.filter(user=request.user, purchased=False)
    orders=Order.objects.filter(user=request.user,ordered=False)
    # print(orders[0])
    if carts.exists() and orders.exists():
        order=orders[0].get_totals
        # print(order)
        return render(request, 'App_Order/cartview.html', context={'carts':carts,'order':order})
    else:
        messages.info(request,"You have no item")
        return redirect('App_Shop:home')
        
@login_required
def remove_cart(request,pk):
    item=get_object_or_404(Product,pk=pk) 
    print("item")
    print(item)
    carts=Cart.objects.get(item=item,user=request.user, purchased=False)
    orders=Order.objects.filter(user=request.user,ordered=False)
    print("orders")
    print(orders)
    if orders.exists():
        order=orders[0]
        print(order)
        r_order=order.orderitems.filter(item=item)
        if r_order.exists():

            order.orderitems.remove(carts)
            carts.delete()
            messages.success(request,"Item deleted")
        
            return redirect('App_Order:viewcart')
    else:
        messages.success(request,"No item found")
        
        return redirect('App_Shop:home')

@login_required
def increase(request,pk):
    item=get_object_or_404(Product,pk=pk)
    
    orders=Order.objects.filter(user=request.user,ordered=False)
    if orders.exists():
        order=orders[0]
        if order.orderitems.filter(item=item).exists():
            carts=Cart.objects.filter(item=item,user=request.user, purchased=False)[0]
            print(carts)
            if carts.quantity >= 1:
                carts.quantity += 1
                print(carts.quantity)
                carts.save()
                messages.info(request,"Item Added")
                return redirect('App_Order:viewcart')
            else:
                messages.info(request, f"{item.name} is not in your cart")
                return redirect("App_Shop:home")
        else:
            messages.info(request,"No item")
            return redirect('App_Order:viewcart')


@login_required
def decrease(request,pk):
    item=get_object_or_404(Product,pk=pk)
    
    orders=Order.objects.filter(user=request.user,ordered=False)
    if orders.exists():
        order=orders[0]
        if order.orderitems.filter(item=item).exists():
            carts=Cart.objects.filter(item=item,user=request.user, purchased=False)[0]
            print(carts)
            if carts.quantity > 1:
                carts.quantity -= 1
                print(carts.quantity)
                carts.save()
                messages.info(request,"Item Removed")
                return redirect('App_Order:viewcart')
            else:
                order.orderitems.remove(carts)
                carts.delete()
                messages.warning(request, f"{item.name} item has been removed from your cart")
                return redirect("App_Order:viewcart")
        else:
            messages.info(request,"NO item")
            return redirect('App_Order:viewcart')
    else:
        messages.info(request, "You don't have an active order")
        return redirect("App_Shop:home")

