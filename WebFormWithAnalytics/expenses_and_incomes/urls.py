from django.urls import path
from . import views

urlpatterns = [
    path('expenses_and_incomes/', views.expenses_and_incomes, name='expenses_and_incomes'),
]