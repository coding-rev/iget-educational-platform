from django.db import models
from django.contrib.auth import get_user_model 
from courses.models import Courses
User = get_user_model()
# Create your models here.

class OrderItem(models.Model):
	user 			= models.ForeignKey(User, on_delete=models.CASCADE)
	ordered 		= models.BooleanField(default=False)
	item 			= models.ForeignKey(Courses, on_delete=models.CASCADE)
	quantity 		= models.IntegerField(default=1)
	
	class Meta:
		verbose_name_plural = 'Order Item'

	def __str__(self):
		return f"{self.quantity} of {self.item.title}"

	def get_total_item_price(self):
		return self.quantity*self.item.price

	def get_total_discount_item_price(self):
		return self.quantity*self.item.discount_price

	def get_amount_saved(self):
		return self.get_total_item_price()-self.get_total_discount_item_price()

	def get_final_price(self):
		if self.item.discount_price:
			return self.get_total_discount_item_price()
		return self.get_total_item_price() 


class Order(models.Model):
	user 				= models.ForeignKey(User, on_delete=models.CASCADE)
	items 				= models.ManyToManyField(OrderItem)
	start_date 			= models.DateTimeField(auto_now_add=True)
	ordered_date 		= models.DateTimeField()
	ordered 			= models.BooleanField(default=False)
	
	class Meta:
		verbose_name_plural = 'Orders'

	def __str__(self):
		return self.user.username

	def get_total(self):
		total = 0
		for order_item in self.items.all():
			total += order_item.get_final_price()
		return total