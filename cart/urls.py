from django.urls import path 
from .import views
app_name ="cart"

urlpatterns =[
	path('', views.Cart, name="cart"),
	path('add-to-cart/<int:pk>', views.add_to_cart, name="add-to-cart"),
	path('remove-from-cart/<int:pk>', views.remove_from_cart, name="remove-from-cart"),
	path('pay-btn', views.payButton, name="pay-btn"),

	path("checkout", views.checkoutPage, name="checkout"),
]