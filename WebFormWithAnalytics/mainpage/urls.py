from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]