"""udemyClone URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from courses import views
from udemyClone import settings

from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('courses.urls')),
    path('register/', include('register.urls')),
    path('cart/', include("cart.urls")),
    path('', include('django.contrib.auth.urls'))
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)