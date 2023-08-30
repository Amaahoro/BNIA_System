from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about_bnia/', views.about, name='about_bnia'),
    path('service/', views.service, name='service'),
    path('service/<str:service_name>/', views.service_details, name='service_details'),
    path('publications/', views.publication, name='publications'),
]
