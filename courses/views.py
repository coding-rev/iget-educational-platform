from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import Courses, Episode
from cart.models import Order
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib import messages

# Create your views here.

User = get_user_model()

def index(request):
	courses     = Courses.objects.all()
	context = {
		"courses":courses,
		
	}
	return render(request, 'home-1.html', context)

@login_required
def listCoursesView(request):
	courses     = Courses.objects.all()
	context     = {
		"courses":courses
	}
	return render(request, 'list-courses.html', context)

@login_required
def CourseDetailView(request, pk):
	course          = Courses.objects.get(id=pk)
	courseEpisodes  = Episode.objects.filter(course=course.id)
	context         = {
		"course":course,
		"courseEpisodes":courseEpisodes
	}
	return render(request, 'course-detail.html', context)


# User specific screens
@login_required
def userAccountPage(request):
	user            = User.objects.get(id=request.user.id)
	context         = {
		"user":user
	}
	return render(request, 'edit-profile.html', context)


class userRegisteredCourses(LoginRequiredMixin, View):
	def get(self, *args, **kwargs):

		try:
			order = Order.objects.filter(user=self.request.user, ordered=True)
			context = {
				'objects':order
			}
			return render(self.request, 'events.html', context)
		except Order.DoesNotExist:
			return render(self.request, 'events.html')

@login_required
def myUploadedCoursesList(request):
	objects =  Courses.objects.filter(author=request.user)
	context ={
		"objects":objects
	}
	return render(request, 'my-uploaded-course.html', context)

@login_required
def deleteCourse(request, pk):
	course 		= Courses.objects.get(id=pk)
	course.delete()
	messages.success(request, "Course deleted successfully")
	return redirect('courses:my-uploaded-courses')


@login_required
def userLessonsPage(request, pk):
	course          = Courses.objects.get(id=pk)
	courseEpisodes  = Episode.objects.filter(course=course.id)
	try:
		currentPlay  	= Episode.objects.filter(course=course.id).first()
	except:
		currentPlay 	= Episode.objects.filter(course=course.id)

	if request.method=="POST":
		course          = Courses.objects.get(id=pk)
		courseEpisodes  = Episode.objects.filter(course=course.id)
		currentPlay 	= Episode.objects.get(course=course.id, id=request.POST.get('episode_id'))
		context 		= {
			"course":course,
			"courseEpisodes":courseEpisodes,
			"currentPlay":currentPlay
		}
		return render(request, "lesson-page.html", context)

	context         = {
		"course":course,
		"courseEpisodes":courseEpisodes,
		"currentPlay":currentPlay
	}
	return render(request, 'lesson-page.html', context)


@login_required
def uploadCourse(request):

	if request.method == 'POST':
		try:
			getImage  		= request.FILES.get('c-image')
			getTitle   		= request.POST.get('c-title')
			getLanguage   	= request.POST.get('c-language')
			getLength   	= request.POST.get('c-length')
			getDescription  = request.POST.get('c-description')
			getFree  		= request.POST.get('c-free')
			getPrice   		= request.POST.get('c-price')
			getDiscount  	= request.POST.get('c-discount')

			try:
				if getFree:
					course 		= Courses.objects.create(
									title=getTitle, description=getDescription,
									author=request.user, language=getLanguage,
									course_length=getLength, free_price=True, image=getImage,
									price=getPrice, discount_price=getDiscount,
									)
				else: 
					course 		= Courses.objects.create(
									title=getTitle, description=getDescription,
									author=request.user, language=getLanguage,
									course_length=getLength, free_price=False, image=getImage,
									price=getPrice, discount_price=getDiscount
									)
			except:
				if getFree:
					course 		= Courses.objects.create(
									title=getTitle, description=getDescription,
									author=request.user, language=getLanguage,
									course_length=getLength, free_price=True, image=getImage,
									price=getPrice
									)
				else: 
					course 		= Courses.objects.create(
									title=getTitle, description=getDescription,
									author=request.user, language=getLanguage,
									course_length=getLength, free_price=False, image=getImage,
									price=getPrice
									)
				
			messages.success(request, "Course uploaded successfully")
			return redirect(reverse('courses:upload-episodes', kwargs={
				'pk':course.id
				}))

		except Exception as e:
			messages.error(request, "Error occured "+str(e))
			return redirect('courses:upload-course')

	return render(request, 'upload-course.html')


@login_required
def uploadEpisodes(request, pk):
	if request.method == 'POST':
		try:
			getCourse 		= Courses.objects.get(id=pk)
			getTitle   	= request.POST.get('e-title')
			getFile  	= request.FILES.get('e-file')
			getDescription = request.POST.get('e-description')

			episode 	= Episode.objects.create(
								title=getTitle, file=getFile, 
								course=getCourse, description=getDescription
								)
			messages.success(request, 'Episode uploaded for course successfully')
			return redirect(reverse('courses:upload-episodes', kwargs={
				'pk':pk
				}))		

		except Exception as e:
			messages.error(request, "Error occured "+ str(e))
			return redirect(reverse('courses:upload-episodes', kwargs={
				'pk':pk
				}))

	return render(request, 'upload-episodes.html')
