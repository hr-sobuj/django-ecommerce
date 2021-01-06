from django import template
from App_Order.models import Order
register = template.Library()
@register.filter
def cart_count(user):
    order=Order.objects.filter(user=user,ordered=False)
    # print(order)
    if order.exists():
        order_count=order[0].orderitems.count()
        return order_count 
    else:
        return 0