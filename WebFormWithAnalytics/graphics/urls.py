from django.urls import path
from . import views

urlpatterns = [
    path('graphics/', views.graphics, name='graphics'),
]