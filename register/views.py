from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login 

User = get_user_model()

# Create your views here.
def registerView(request):
	if request.method == 'POST':
		Getfirst_name  		= request.POST.get("first-name")
		Getlast_name 		= request.POST.get("last-name")
		Getusername   		= request.POST.get("username")
		Getemail  			= request.POST.get("email")
			
		Getpassword     	= request.POST.get("password")
		GetconfirmPassword 	= request.POST.get("confirm-password")
			
		if Getpassword  	!= GetconfirmPassword:
			messages.error(request, "Passwords do not match")
		else:
			if User.objects.filter(username=Getusername).exists():
				messages.error(request, "Username not available")
				
			elif User.objects.filter(email=Getemail).exists():
				messages.error(request, "User with email already exist")
							
			else:	
				try:
					user 		= User.objects.create_user(
									username=Getusername, first_name=Getfirst_name,
									last_name=Getlast_name, email=Getemail,
								)
					user.set_password(Getpassword)
					user.save()
					user 		= authenticate(request, username=Getusername, password=Getpassword)
					login(request, user)
					messages.success(request, "Account created successfully")
					return redirect('courses:homepage')
			
				except Exception as e:
					messages.error(request, str(e))
	return render(request, 'register.html')


