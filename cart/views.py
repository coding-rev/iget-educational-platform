from django.shortcuts import render,  get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages

from courses.models import Courses
from .models import OrderItem, Order
# Create your views here.

@login_required
def Cart(request):
	try:
		orders          = Order.objects.get(user=request.user, ordered=False)
	except:
		orders 			= False
	context         = {
		"objects":orders
	}
	return render(request, 'shopping-cart.html', context)


@login_required
def checkoutPage(request):
	orders          = Order.objects.get(user=request.user, ordered=False)
	
	context         = {
		"objects":orders
	}
	return render(request, 'checkout-detail.html', context)

def payButton(request):
	orders          = Order.objects.get(user=request.user, ordered=False)
	orders.ordered = True 
	orders.save()
	messages.success(request, "Payment successful.")
	return redirect('/')




@login_required
def add_to_cart(request, pk):
	item = get_object_or_404(Courses, id=pk)
	order_item, created = OrderItem.objects.get_or_create(
		item=item,
		user= request.user,
		ordered=False
	)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		#check if the order item is in the order
		if order.items.filter(item__pk=item.pk).exists():
			messages.info(request, "Item already in cart")
		else:
			messages.info(request, "This item was added to your cart successfully")
			order.items.add(order_item)

	else:
		ordered_date = timezone.now()
		order = Order.objects.create(
			user=request.user, ordered_date=ordered_date)
		order.items.add(order_item)
		messages.info(request, "This item was added to your cart successfully")
	url = request.META.get('HTTP_REFERER')
	return HttpResponseRedirect(url)


@login_required
def remove_from_cart(request, pk):
	item = get_object_or_404(Courses, id=pk)
	order_qs = Order.objects.filter(
		user=request.user,
		ordered=False
	)
	if order_qs.exists():
		order = order_qs[0]
		#check if the order item is in the order
		if order.items.filter(item__pk=item.pk).exists():
			order_item = OrderItem.objects.filter(
				item=item,
				user=request.user,
				ordered=False
			)[0]
			order.items.remove(order_item)
			messages.info(request, "This item was removed from your cart successfully")
			url = request.META.get('HTTP_REFERER')
			return HttpResponseRedirect(url)
		else:
			# add a message saying the user doesn't have an order
			messages.info(request, "This item was not in your cart")
			url = request.META.get('HTTP_REFERER')
			return HttpResponseRedirect(url)
	else:
		#add a message saying the user doesn't have an order
		messages.info(request, "You do not have an active order")
		url = request.META.get('HTTP_REFERER')
		return HttpResponseRedirect(url)
	url = request.META.get('HTTP_REFERER')
	return HttpResponseRedirect(url)



