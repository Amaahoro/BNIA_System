from django.shortcuts import redirect, render
from django.contrib import messages
from django.conf import settings

from .models import *


# Create your views here.
def handle_not_found(request, exception):
    return render(request, '404.html')



def home(request):
    services = Service.objects.filter()[:3]
    context={
        'title': 'Home',
        'home_active': 'active',
        'services': services,
    }
    return render(request, 'home.html', context)



def about(request):
    context={
        'title': 'About Us',
        'about_active': 'active',
    }
    return render(request, 'about.html', context)



def service(request):
    services = Service.objects.filter()
    context={
        'title': 'Services',
        'service_active': 'active',
        'services': services,
    }
    return render(request, 'service.html', context)



def service_details(request, service_name):
    if Service.objects.filter(service_name=service_name).exists():
        data_found = Service.objects.get(service_name=service_name)
        context={
            'title': data_found.service_name,
            'service_active': 'active',
            'service': data_found,
        }
        return render(request, 'service_details.html', context)
    else:
        messages.error(request, ('Service not found!'))
        redirect(service)



def publication(request):
    found_data = Publication.objects.filter()
    context={
        'title': 'Publications',
        'pub_active': 'active',
        'publications': found_data,
    }
    return render(request, 'publication.html', context)

