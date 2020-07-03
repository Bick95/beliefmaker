from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('solution/', views.home_solution, name="solve"),
    path('vis/', views.home_solution, name="vis"),
]
