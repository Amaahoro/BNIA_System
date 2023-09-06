from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout, update_session_auth_hash

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



def staffLogin(request):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        return redirect(adm_dashboard)
    elif request.user.is_authenticated and request.user.is_chief_commune == True:
        return redirect(chief_dashboard)
    else:
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None and user.is_nationalAdministrator == True:
                login(request, user)
                messages.success(request, ('Hi '+user.first_name+', Welcome back to the dashboard!'))
                return redirect(adm_dashboard)
            elif user is not None and user.is_chief_commune == True:
                login(request, user)
                messages.success(request, ('Hi '+user.first_name+', Welcome back to the dashboard!'))
                return redirect(chief_dashboard)
            else:
                messages.error(
                    request, ('User Email or Password is not correct! Try agin...'))
                return redirect(staffLogin)
        else:
            context = {'title': 'Staff Login', }
            return render(request, 'management/login.html', context)



@login_required(login_url='staff_login')
def staffLogout(request):
    logout(request)
    messages.info(request, ('You are now Logged out.'))
    return redirect(staffLogin)




# ==========================================================
# natinal administrator
# ==========================================================

@login_required(login_url='staff_login')
def adm_dashboard(request):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        # getting data
        citizens = Citizen.objects.filter()

        context = {
            'title': 'National Administrator - Dashboard',
            'dash_active': 'active',
            'citizens': citizens,
        }
        return render(request, 'management/administrator/dashboard.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='staff_login')
def adm_profile(request):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        if 'update_password' in request.POST:
            old_password = request.POST.get("old_pass")
            new_password = request.POST.get("pass1")
            confirmed_new_password = request.POST.get("pass2")

            if old_password and new_password and confirmed_new_password:
                user = get_user_model().objects.get(email=request.user.email)

                if not user.check_password(old_password):
                    messages.error(
                        request, "Your old password is not correct!")
                    return redirect(adm_profile)

                else:
                    if len(new_password) < 5:
                        messages.warning(request, "Your password is too weak!")
                        return redirect(adm_profile)

                    elif new_password != confirmed_new_password:
                        messages.error(
                            request, "Your new password not match the confirm password !")
                        return redirect(adm_profile)

                    else:
                        user.set_password(new_password)
                        user.save()
                        update_session_auth_hash(request, user)

                        messages.success(
                            request, "Your password has been changed successfully.!")
                        return redirect(adm_profile)

            else:
                messages.error(request, "Error , All fields are required !")
                return redirect(adm_profile)

        else:
            context = {
                'title': 'National Administrator - Profile',
            }
            return render(request, 'management/administrator/profile.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='registrar_login')
def adm_services(request):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        if 'new_service' in request.POST:
            service_name = request.POST.get("service_name")
            requirements = request.POST.get("requirements")

            if service_name:
                # service_name=service_name.upper()
                found_data = Service.objects.filter(service_name=service_name)
                if found_data:
                    messages.warning(request, "The service " +
                                     service_name+", Already exist.")
                    return redirect(adm_services)
                else:
                    # add new service
                    add_service = Service(
                        recorded_by=request.user,
                        service_name=service_name,
                        requirements=requirements,
                    )
                    add_service.save()

                    messages.success(
                        request, "New Service created successfully.")
                    return redirect(adm_services)
            else:
                messages.error(request, "Error , Service name is required!")
                return redirect(adm_services)
        else:
            # request_data = Application.objects.filter(status="Waiting")
            # getting services
            ServiceData = Service.objects.filter().order_by('service_name')
            context = {
                'title': 'National Administrator - Service List',
                'service_active': 'active',
                'services': ServiceData,
                # 'request_data': request_data,
            }
            return render(request, 'management/administrator/service_list.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='registrar_login')
def adm_serviceDetails(request, pk):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        service_id = pk
        # getting service
        if Service.objects.filter(id=service_id).exists():
            # if exists
            foundData = Service.objects.get(id=service_id)

            if 'update_service' in request.POST:
                # Retrieve the form data from the request
                service_name = request.POST.get('service_name')
                requirements = request.POST.get('requirements')

                if service_name:
                    if Service.objects.filter(service_name=service_name).exclude(id=service_id):
                        messages.warning(
                            request, "Service name already exist.")
                        return redirect(adm_serviceDetails, pk)
                    else:
                        # Update Service
                        service_updated = Service.objects.filter(id=service_id).update(
                            service_name=service_name,
                            requirements=requirements,
                        )
                        if service_updated:
                            messages.success(
                                request, "Service "+service_name+", Updated successfully.")
                            return redirect(adm_serviceDetails, pk)
                        else:
                            messages.error(request, ('Process Failed.'))
                            return redirect(adm_serviceDetails, pk)
                else:
                    messages.error(request, ('Service name is required.'))
                    return redirect(adm_serviceDetails, pk)

            elif 'delete_service' in request.POST:
                # Delete Service
                delete_service = Service.objects.get(id=service_id)
                delete_service.delete()
                messages.success(request, "Service info deleted successfully.")
                return redirect(adm_services)

            else:
                # request_data = Application.objects.filter(status="Waiting")
                context = {
                    'title': 'National Administrator - Service Info',
                    'service_active': 'active',
                    'service': foundData,
                    # 'request_data': request_data,
                }
                return render(request, 'management/administrator/service_details.html', context)
        else:
            messages.error(request, ('Service not found'))
            return redirect(adm_services)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)




@login_required(login_url='registrar_login')
def adm_provinces(request):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        if 'new_province' in request.POST:
            province_name = request.POST.get("province_name")

            if province_name:
                # province_name=province_name.upper()
                found_data = Province.objects.filter(province_name=province_name)
                if found_data:
                    messages.warning(request, "The province " +
                                     province_name+", Already exist.")
                    return redirect(adm_provinces)
                else:
                    # add new province
                    addProvince = Province(
                        province_name=province_name,
                    )
                    addProvince.save()

                    messages.success(
                        request, "New Province created successfully.")
                    return redirect(adm_provinces)
            else:
                messages.error(request, "Error , Province name is required!")
                return redirect(adm_provinces)
        else:
            # request_data = Application.objects.filter(status="Waiting")
            # getting provinces
            ProvinceData = Province.objects.filter().order_by('province_name')
            context = {
                'title': 'National Administrator - Province List',
                'province_active': 'active',
                'provinces': ProvinceData,
                # 'request_data': request_data,
            }
            return render(request, 'management/administrator/province_list.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='registrar_login')
def adm_provinceDetails(request, pk):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        province_id = pk
        # getting province
        if Province.objects.filter(id=province_id).exists():
            # if exists
            foundData = Province.objects.get(id=province_id)

            if 'update_province' in request.POST:
                # Retrieve the form data from the request
                province_name = request.POST.get('province_name')

                if province_name:
                    if Province.objects.filter(province_name=province_name).exclude(id=province_id):
                        messages.warning(
                            request, "Province name already exist.")
                        return redirect(adm_provinceDetails, pk)
                    else:
                        # Update province
                        province_updated = Province.objects.filter(id=province_id).update(
                            province_name=province_name,
                        )
                        if province_updated:
                            messages.success(
                                request, "Province "+province_name+", Updated successfully.")
                            return redirect(adm_provinceDetails, pk)
                        else:
                            messages.error(request, ('Process Failed.'))
                            return redirect(adm_provinceDetails, pk)
                else:
                    messages.error(request, ('Province name is required.'))
                    return redirect(adm_provinceDetails, pk)

            elif 'delete_province' in request.POST:
                # Delete province
                delete_province = Province.objects.get(id=province_id)
                delete_province.delete()
                messages.success(request, "Province info deleted successfully.")
                return redirect(adm_provinces)

            else:
                # request_data = Application.objects.filter(status="Waiting")
                context = {
                    'title': 'National Administrator - Province Info',
                    'province_active': 'active',
                    'province': foundData,
                    # 'request_data': request_data,
                }
                return render(request, 'management/administrator/province_details.html', context)
        else:
            messages.error(request, ('Province not found'))
            return redirect(adm_provinces)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)




@login_required(login_url='registrar_login')
def adm_communes(request):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        if 'new_commune' in request.POST:
            province_id = request.POST.get("province")
            commune_name = request.POST.get("commune_name")

            if province_id and commune_name:
                # commune_name=commune_name.upper()
                found_data = Commune.objects.filter(province=province_id,commune_name=commune_name)
                if found_data:
                    messages.warning(request, "The Commune " +
                                     commune_name+", Already exist.")
                    return redirect(adm_communes)
                else:
                    # add new commune
                    addCommune = Commune(
                        province=Province.objects.get(id=province_id),
                        commune_name=commune_name
                    )
                    addCommune.save()

                    messages.success(
                        request, "New Commune created successfully.")
                    return redirect(adm_communes)
            else:
                messages.error(request, "Error , All fields are required!")
                return redirect(adm_communes)
        else:
            # request_data = Application.objects.filter(status="Waiting")
            # getting province
            ProvinceData = Province.objects.filter().order_by('province_name')
            # getting communes
            CommuneData = Commune.objects.filter().order_by('province','commune_name')
            context = {
                'title': 'National Administrator - Commune List',
                'commune_active': 'active',
                'communes': CommuneData,
                'provinces': ProvinceData,
                # 'request_data': request_data,
            }
            return render(request, 'management/administrator/commune_list.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='registrar_login')
def adm_communeDetails(request, pk):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        commune_id = pk
        # getting commune
        if Commune.objects.filter(id=commune_id).exists():
            # if exists
            foundData = Commune.objects.get(id=commune_id)

            if 'update_commune' in request.POST:
                # Retrieve the form data from the request
                province_id = request.POST.get("province")
                commune_name = request.POST.get("commune_name")

                if province_id and commune_name:
                    if Commune.objects.filter(province=province_id,commune_name=commune_name).exclude(id=commune_id):
                        messages.warning(
                            request, "Commune name already exist.")
                        return redirect(adm_communeDetails, pk)
                    else:
                        # Update Commune
                        commune_updated = Commune.objects.filter(id=commune_id).update(
                            province=Province.objects.get(id=province_id),
                            commune_name=commune_name
                        )
                        if commune_updated:
                            messages.success(
                                request, "Commune "+commune_name+", Updated successfully.")
                            return redirect(adm_communeDetails, pk)
                        else:
                            messages.error(request, ('Process Failed.'))
                            return redirect(adm_communeDetails, pk)
                else:
                    messages.error(request, ('Commune name is required.'))
                    return redirect(adm_communeDetails, pk)

            elif 'delete_commune' in request.POST:
                # Delete commune
                delete_commune = Commune.objects.get(id=commune_id)
                delete_commune.delete()
                messages.success(request, "Commune info deleted successfully.")
                return redirect(adm_communes)

            else:
                # request_data = Application.objects.filter(status="Waiting")
                
                # getting province
                ProvinceData = Province.objects.filter().order_by('province_name')
                context = {
                    'title': 'National Administrator - Commune Info',
                    'commune_active': 'active',
                    'commune': foundData,
                    'provinces': ProvinceData,
                    # 'request_data': request_data,
                }
                return render(request, 'management/administrator/commune_details.html', context)
        else:
            messages.error(request, ('Commune not found'))
            return redirect(adm_communes)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)




@login_required(login_url='registrar_login')
def adm_collines(request):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        if 'new_colline' in request.POST:
            commune_id = request.POST.get("commune")
            colline_name = request.POST.get("colline_name")

            if commune_id and colline_name:
                # colline_name=colline_name.upper()
                found_data = Colline.objects.filter(commune=commune_id,colline_name=colline_name)
                if found_data:
                    messages.warning(request, "The Commune " +
                                     colline_name+", Already exist.")
                    return redirect(adm_collines)
                else:
                    # add new colline
                    addColline = Colline(
                        commune=Commune.objects.get(id=commune_id),
                        colline_name=colline_name
                    )
                    addColline.save()

                    messages.success(
                        request, "New Colline created successfully.")
                    return redirect(adm_collines)
            else:
                messages.error(request, "Error , All fields are required!")
                return redirect(adm_collines)
        else:
            # request_data = Application.objects.filter(status="Waiting")
            # getting commune
            CommuneData = Commune.objects.filter().order_by('commune_name')
            # getting collines
            CollineData = Colline.objects.filter().order_by('commune','colline_name')
            context = {
                'title': 'National Administrator - Colline List',
                'colline_active': 'active',
                'collines': CollineData,
                'communes': CommuneData,
                # 'request_data': request_data,
            }
            return render(request, 'management/administrator/colline_list.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='registrar_login')
def adm_collineDetails(request, pk):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        colline_id = pk
        # getting commune
        if Colline.objects.filter(id=colline_id).exists():
            # if exists
            foundData = Colline.objects.get(id=colline_id)

            if 'update_colline' in request.POST:
                # Retrieve the form data from the request
                commune_id = request.POST.get("commune")
                colline_name = request.POST.get("colline_name")

                if commune_id and colline_name:
                    if Colline.objects.filter(commune=commune_id,colline_name=colline_name).exclude(id=colline_id):
                        messages.warning(
                            request, "Colline name already exist.")
                        return redirect(adm_collineDetails, pk)
                    else:
                        # Update Colline
                        colline_updated = Colline.objects.filter(id=colline_id).update(
                            commune=Commune.objects.get(id=commune_id),
                            colline_name=colline_name
                        )
                        if colline_updated:
                            messages.success(
                                request, "Colline "+colline_name+", Updated successfully.")
                            return redirect(adm_collineDetails, pk)
                        else:
                            messages.error(request, ('Process Failed.'))
                            return redirect(adm_collineDetails, pk)
                else:
                    messages.error(request, ('Colline name is required.'))
                    return redirect(adm_collineDetails, pk)

            elif 'delete_colline' in request.POST:
                # Delete colline
                delete_colline = Colline.objects.get(id=colline_id)
                delete_colline.delete()
                messages.success(request, "Colline info deleted successfully.")
                return redirect(adm_collines)

            else:
                # request_data = Application.objects.filter(status="Waiting")
                
                # getting commune
                communeData = Commune.objects.filter().order_by('commune_name')
                context = {
                    'title': 'National Administrator - Colline Info',
                    'colline_active': 'active',
                    'colline': foundData,
                    'communes': communeData,
                    # 'request_data': request_data,
                }
                return render(request, 'management/administrator/colline_details.html', context)
        else:
            messages.error(request, ('Colline not found'))
            return redirect(adm_collines)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)







# ==========================================================
# chief commune
# ==========================================================

@login_required(login_url='staff_login')
def chief_dashboard(request):
    if request.user.is_authenticated and request.user.is_chief_commune == True:
        # getting data
        citizens = Citizen.objects.filter()

        context = {
            'title': 'National Administrator - Dashboard',
            'dash_active': 'active',
            'citizens': citizens,
        }
        return render(request, 'management/commune/dashboard.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='staff_login')
def chief_profile(request):
    if request.user.is_authenticated and request.user.is_chief_commune == True:
        if 'update_password' in request.POST:
            old_password = request.POST.get("old_pass")
            new_password = request.POST.get("pass1")
            confirmed_new_password = request.POST.get("pass2")

            if old_password and new_password and confirmed_new_password:
                user = get_user_model().objects.get(email=request.user.email)

                if not user.check_password(old_password):
                    messages.error(
                        request, "Your old password is not correct!")
                    return redirect(chief_profile)

                else:
                    if len(new_password) < 5:
                        messages.warning(request, "Your password is too weak!")
                        return redirect(chief_profile)

                    elif new_password != confirmed_new_password:
                        messages.error(
                            request, "Your new password not match the confirm password !")
                        return redirect(chief_profile)

                    else:
                        user.set_password(new_password)
                        user.save()
                        update_session_auth_hash(request, user)

                        messages.success(
                            request, "Your password has been changed successfully.!")
                        return redirect(chief_profile)

            else:
                messages.error(request, "Error , All fields are required !")
                return redirect(chief_profile)

        else:
            context = {
                'title': 'National Administrator - Profile',
            }
            return render(request, 'management/commune/profile.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)

