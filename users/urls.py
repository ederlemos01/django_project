from django.urls import path
from . import views 

urlpatterns = [
    
    path('register/', views.user_register),
    path('<str:username>/', views.user_detail),
]