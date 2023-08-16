from django.shortcuts import redirect, render
from django.contrib import messages
from django.conf import settings

from .models import *


# Create your views here.
def handle_not_found(request, exception):
    return render(request, 'management/404.html')



def home(request):
    return render(request, 'management/index.html')

