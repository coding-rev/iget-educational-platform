from django.contrib import admin
from .models import *

# Register your models here.
admin.site.site_title  	= "iGet Admin"
admin.site.site_header	= "iGet Admin"

admin.site.register(Courses)
admin.site.register(Rate)
admin.site.register(Episode)
admin.site.register(CourseSection)
