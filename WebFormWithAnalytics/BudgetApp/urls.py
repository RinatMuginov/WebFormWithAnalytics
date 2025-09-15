from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')), 
    path('', include('mainpage.urls')), 
    path('', include('expenses_and_incomes.urls')), 
    path('', include('graphics.urls')), 
    path('', include('profilepage.urls')), 
]