from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView,DetailView 
from App_Shop.models import Product
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

class Home(ListView):
    model = Product
    # context_object_name = 'products_list'
    template_name='App_Shop/home.html'

class ProductDetailView(DetailView):
    model = Product
    template_name = "App_Shop/product_detail.html"

def modalView(request,pk):
    print(pk)
    product=Product.objects.get(pk=pk)
    print(product)
    context={'product':product}
    if product:
        quick_view=render_to_string('modeltemp.html',{
            'context':context,
            'request':request
        })
        return JsonResponse({'quick_view':quick_view})
    # return render(request, "modaltemp.html", context={'product':item})


    

