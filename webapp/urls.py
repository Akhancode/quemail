
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('',include('website.urls')),
    path('automate/',include('website.urls')),
    path('One_bulk/',include('website.urls')),
    path('admin/', admin.site.urls),
]
