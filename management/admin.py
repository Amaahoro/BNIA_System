from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(Province)
admin.site.register(Commune)
admin.site.register(Colline)
admin.site.register(Citizen)
admin.site.register(CitizenParent)
admin.site.register(IDCardRegistration)
admin.site.register(LostIDCardReport)