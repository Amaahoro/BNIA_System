from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about_bnia/', views.about, name='about_bnia'),
    path('service/', views.service, name='service'),
    path('service/<str:service_name>/', views.service_details, name='service_details'),
    path('publications/', views.publication, name='publications'),
    
    
    # staff
    path('staff/login/', views.staffLogin, name='staff_login'),
    path('staff/logout/', views.staffLogout, name='staff_logout'),
    # national administator
    path('bnia/administrator/dashboard/', views.adm_dashboard, name='adm_dashboard'),
    path('bnia/administrator/profile/', views.adm_profile, name='adm_profile'),
]
