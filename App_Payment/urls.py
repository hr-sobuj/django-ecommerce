from django.urls import path
from App_Payment import views 

app_name='App_Payment'

urlpatterns = [
    path('checkout/',views.CheckoutView,name='checkout'),
    path('pay/',views.PaymentGateWay,name='pay'),
    path('complete/',views.complete,name='complete'),
    path('purchas/<tran_id>/<val_id>/<tran_date>/<amount>/<card_type>/',views.purchas,name='purchas'),
    path('receipt/<tran_id>/<val_id>/<tran_date>/<amount>/<card_type>/<save_address>',views.receipt,name='receipt'),
    path('pdf/<tran_id>/<val_id>/<tran_date>/<amount>/<card_type>/<save_address>',views.pdfgenerate,name='pdf'),
]
