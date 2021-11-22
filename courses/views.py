from django.shortcuts import render
from django.http import HttpResponse
from .models import Courses, Episode
from cart.models import Order
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
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
            print(len(order))
            context = {
                'objects':order
            }
            return render(self.request, 'events.html', context)
        except Order.DoesNotExist:
            return render(self.request, 'events.html')

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
	return render(request, 'upload-course.html')


