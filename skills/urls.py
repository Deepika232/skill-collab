from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.create_skill, name='create'),
    # Placeholder for skill-related views
] 