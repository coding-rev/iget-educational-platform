from django.db import models
from django.contrib.auth import get_user_model 

User = get_user_model()

# Create your models here.
class Rate(models.Model):
	rate_number  		= models.IntegerField(range(0,5))


class CourseSection(models.Model):
	section_title  		= models.CharField(max_length=225,blank=True,null=True)
	section_number  	= models.IntegerField(blank=True,null=True)
	episodes  			= models.ManyToManyField('Episode',blank=True)

	def total_length(self):
		total=Decimal(0.00)
		for episode in self.episodes.all():
			total+=episode.length
		return get_timer(total,type='min')


class Comment(models.Model):
	user  			= models.ForeignKey(User,on_delete=models.CASCADE)
	message  		= models.TextField()
	created  		= models.DateTimeField(auto_now=True)



class Courses(models.Model):
	title			= models.CharField(max_length=225)
	description		= models.TextField()
	created			= models.DateTimeField(auto_now_add=True)
	updated			= models.DateTimeField(auto_now=True)
	rating 			= models.ManyToManyField('Rate',blank=True)
	author  		= models.ForeignKey(User, on_delete=models.CASCADE)
	student_rating	= models.IntegerField(default=0)
	language  		= models.CharField(max_length=225)
	course_length  	= models.CharField(default=0,max_length=20)
	course_sections = models.ManyToManyField('CourseSection',blank=True)
	comment  		= models.ManyToManyField('Comment',blank=True)
	image  			= models.ImageField()
	free_price 		= models.BooleanField(default=False, verbose_name="Free Course")
	price  			= models.IntegerField()
	discount_price  = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return self.title 
	class Meta:
		verbose_name_plural = "Courses"

class Episode(models.Model):
	title  			= models.CharField(max_length=225)
	file  			= models.FileField()
	length  		= models.IntegerField()
	course 			= models.ForeignKey(Courses, on_delete=models.CASCADE) 	
	description 	= models.CharField(max_length=30)		 

	def get_video_length(self):
		try:
			video=MP4(self.file)
			return video.info.length
			
		except:
			return 0.0

	def get_video_length_time(self):
		return get_timer(self.length)
	
	def get_absolute_url(self):
		return self.file.url

	def __str__(self):
		return self.course.title
	
		
	
	def save(self,*args, **kwargs):
		self.length=self.get_video_length()
		# print(self.length)
		# print(self.file.path)
		
		
		return super().save(*args, **kwargs)


