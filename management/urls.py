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
    path('bnia/administrator/services/', views.adm_services, name='adm_services'),
    path('bnia/administrator/services/<int:pk>/service_details/', views.adm_serviceDetails, name='adm_serviceDetails'),
    path('bnia/administrator/territorial/provinces/', views.adm_provinces, name='adm_provinces'),
    path('bnia/administrator/territorial/provinces/<int:pk>/province_details/', views.adm_provinceDetails, name='adm_provinceDetails'),
    path('bnia/administrator/territorial/communes/', views.adm_communes, name='adm_communes'),
    path('bnia/administrator/territorial/communes/<int:pk>/commune_details/', views.adm_communeDetails, name='adm_communeDetails'),
    path('bnia/administrator/territorial/collines/', views.adm_collines, name='adm_collines'),
    path('bnia/administrator/territorial/collines/<int:pk>/colline_details/', views.adm_collineDetails, name='adm_collineDetails'),
    path('bnia/administrator/commune_chiefs/', views.adm_communeChiefs, name='adm_communeChiefs'),
    path('bnia/administrator/commune_chiefs/<int:pk>/chief_details/', views.adm_communeChiefDetails, name='adm_communeChiefDetails'),
    path('bnia/administrator/publications/', views.adm_publications, name='adm_publications'),
    path('bnia/administrator/publications/<int:pk>/publication_details/', views.adm_publicationDetails, name='adm_publicationDetails'),
    
    # national chief commune
    path('bnia/chief_communer/dashboard/', views.chief_dashboard, name='chief_dashboard'),
    path('bnia/chief_communer/profile/', views.chief_profile, name='chief_profile'),
    path('bnia/chief_communer/services/', views.chief_services, name='chief_services'),
    path('bnia/chief_communer/services/<int:pk>/service_details/', views.chief_serviceDetails, name='chief_serviceDetails'),
    path('bnia/chief_communer/publications/', views.chief_publications, name='chief_publications'),
    path('bnia/chief_communer/publications/<int:pk>/publication_details/', views.chief_publicationDetails, name='chief_publicationDetails'),
]
