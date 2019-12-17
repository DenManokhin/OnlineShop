from django import template
from django.db.models import Sum

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        order = user.order_set.filter(is_paid=False).first()
        if order:
            amount = order.orderitem_set.aggregate(Sum('amount'))['amount__sum']
            if not amount:
                return 0
            else:
                return amount
    return 0
