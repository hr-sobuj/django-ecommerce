from django.urls import path
from App_Order import views 

app_name="App_Order"

urlpatterns = [
    path('cart/<pk>/',views.add_to_cart,name='cart'),
    path('viewcart/',views.cart_template,name='viewcart'),
    path('removecart/<pk>/',views.remove_cart,name='removecart'),
    path('increament/<pk>/',views.increase,name='increament'),
    path('decreament/<pk>/',views.decrease,name='decreament'),
]
