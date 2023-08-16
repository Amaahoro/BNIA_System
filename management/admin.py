from django.contrib import admin
from . models import *

# Register your models here.

class CollineInline(admin.StackedInline):
    model = Colline
    extra = 0

class CommuneInline(admin.StackedInline):
    model = Commune
    inlines = [CollineInline]
    extra = 0

class CitizenParentInline(admin.StackedInline):
    model = CitizenParent
    extra = 0


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('province_name','all_commune',)
    fieldsets = (
        ('Province Info', {'fields': ('province_name',)}),
    )
    add_fieldsets = (
        ('Register New Province', {'fields': ('province_name',)}),
    )
    search_fields = ('province_name',)
    ordering = ('province_name',)
    list_per_page = 10
    inlines = [
        CommuneInline,
    ]
    def all_commune(self, obj):
        return obj.communes.count()


@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display = ('commune_name','all_collines','province',)
    list_filter = ('province',)
    fieldsets = (
        ('Commune Info', {'fields': ('province', 'commune_name',)}),
    )
    add_fieldsets = (
        ('Register New Commune', {'fields': ('province', 'commune_name',)}),
    )
    search_fields = ('commune_name',)
    ordering = ('province',)
    list_per_page = 20
    inlines = [
        CollineInline,
    ]
    def all_collines(self, obj):
        return obj.collines.count()



@admin.register(Colline)
class Colline(admin.ModelAdmin):
    list_display = ('colline_name', 'commune',)
    list_filter = ('commune',)
    fieldsets = (
        ('Product Details', {'fields': ('colline_name', 'commune',)}),
    )
    add_fieldsets = (
        ('Register New Product', {'fields': ('colline_name', 'commune', )}),
    )
    search_fields = ('colline_name',)
    ordering = ('commune',)
    list_per_page = 20



@admin.register(Citizen)
class CitizenAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','gender','birth_place','nationality','birthdate','image')
    list_filter = ('birthdate',)
    fieldsets = (
        ('Citizen Info', {'fields': (
            'recorded_by', 'first_name', 'last_name', 'gender', 'birth_place', 'nationality', 'nid_number', 'birthdate', 'picture', 'createdDate',
        )}),
    )
    add_fieldsets = (
        ('Register New Citizen', {'fields': (
            'recorded_by', 'first_name', 'last_name', 'gender', 'birth_place', 'nationality', 'nid_number', 'birthdate', 'picture', 'createdDate',
        )}),
    )
    search_fields = ('first_name', 'last_name', 'nid_number',)
    ordering = ('createdDate',)
    list_per_page = 20
    inlines = [
        CitizenParentInline,
    ]

    def get_readonly_fields(self, request, obj=None):
        return ['createdDate',]


@admin.register(CitizenParent)
class CitizenParentAdmin(admin.ModelAdmin):
    list_display = ('parent', 'first_name', 'last_name', 'citizen',)
    list_filter = ('parent',)
    fieldsets = (
        ('Citizen parent Info', {'fields': ('parent', 'first_name', 'last_name', 'citizen',)}),
    )
    add_fieldsets = (
        ('Register New Citizen parent', {'fields': ('parent', 'first_name', 'last_name', 'citizen',)}),
    )
    search_fields = ('first_name', 'last_name',)
    ordering = ('citizen',)
    list_per_page = 20



@admin.register(IDCardRegistration)
class IDCardRegistrationAdmin(admin.ModelAdmin):
    list_display = ('citizen','resident_address','picture', 'registration_date',)
    list_filter = ('registration_date',)
    fieldsets = (
        ('ID Card Registration Info', {'fields': ('recorded_by','citizen','resident_address','picture','registration_date',)}),
    )
    add_fieldsets = (
        ('New ID Card Registration', {'fields': ('recorded_by','citizen','resident_address','picture','registration_date',)}),
    )
    ordering = ('registration_date',)
    list_per_page = 20

    def get_readonly_fields(self, request, obj=None):
        return ['registration_date',]



@admin.register(RegisteredIDCard)
class RegisteredIDCardAdmin(admin.ModelAdmin):
    list_display = ('citizen','card_number','created_date','is_taken','taken_date',)
    list_filter = ('is_taken',)
    fieldsets = (
        ('ID Card Registration Info', {'fields': ('recorded_by','citizen','card_number','created_date','is_taken','taken_date',)}),
    )
    add_fieldsets = (
        ('New ID Card Registration', {'fields': ('recorded_by','citizen','card_number','created_date','is_taken','taken_date',)}),
    )
    search_fields = ('card_number',)
    ordering = ('is_taken',)
    list_per_page = 20

    def get_readonly_fields(self, request, obj=None):
        return ['created_date',]



@admin.register(LostIDCardReport)
class LostIDCardReportAdmin(admin.ModelAdmin):
    list_display = ('citizen','card_number','date_lost','description','contact_info','created_date',)
    list_filter = ('created_date',)
    fieldsets = (
        ('Lost ID Card Report Info', {'fields': ('recorded_by','citizen','card_number','date_lost','description','contact_info','created_date',)}),
    )
    add_fieldsets = (
        ('New Lost ID Card Report', {'fields': ('recorded_by','citizen','card_number','date_lost','description','contact_info','created_date',)}),
    )
    search_fields = ('card_number','contact_info',)
    ordering = ('created_date',)
    list_per_page = 20

    def get_readonly_fields(self, request, obj=None):
        return ['created_date',]