from django import template
from cart.models import Order

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs= Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0

@register.filter
def registered_courses_count(user):
    if user.is_authenticated:
        total_count = 0
        qs= Order.objects.filter(user=user, ordered=True)
        print(len(qs))
        if qs.exists():
            for oneOrder in qs:
                total_count += oneOrder.items.count()
        return total_count
    return 0