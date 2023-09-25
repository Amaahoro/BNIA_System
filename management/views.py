from django.utils import timezone
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



@login_required(login_url='staff_login')
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



@login_required(login_url='staff_login')
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




@login_required(login_url='staff_login')
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



@login_required(login_url='staff_login')
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




@login_required(login_url='staff_login')
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



@login_required(login_url='staff_login')
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




@login_required(login_url='staff_login')
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



@login_required(login_url='staff_login')
def adm_collineDetails(request, pk):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        colline_id = pk
        # getting colline
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




@login_required(login_url='staff_login')
def adm_communeChiefs(request):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        if 'new_chief' in request.POST:
            # Retrieve the form data from the request
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone')
            commune_id = request.POST.get('commune')

            if first_name and last_name and email and gender and commune_id:
                if get_user_model().objects.filter(email=email):
                    messages.warning(request, "Email already exist.")
                    return redirect(adm_communeChiefs)
                elif get_user_model().objects.filter(commune=commune_id):
                    messages.warning(request, "Commune already assigned to a chief.")
                    return redirect(adm_communeChiefs)
                else:
                    # Create new User as chief_commune
                    user =  get_user_model().objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        password='user12345',
                        gender=gender,
                        is_chief_commune=True,
                        commune=Commune.objects.get(id=commune_id),
                        phone=phone,
                    )
                    if user:
                        messages.success(request, "Chief "+first_name+" "+last_name+", created successfully.")
                        return redirect(adm_communeChiefs)
                    else:
                        messages.error(request, ('Process Failed.'))
                        return redirect(adm_communeChiefs)
            else:
                messages.error(request, "Error , All fields are required!")
                return redirect(adm_communeChiefs)
        else:
            # request_data = Application.objects.filter(status="Waiting")
            # getting commune
            CommuneData = Commune.objects.filter().order_by('commune_name')
            # getting chiefs
            ChiefData = get_user_model().objects.filter(is_chief_commune=True).order_by('commune')
            context = {
                'title': 'National Administrator - Commune Chiefs List',
                'chief_active': 'active',
                'chiefs': ChiefData,
                'communes': CommuneData,
                # 'request_data': request_data,
            }
            return render(request, 'management/administrator/chiefCommune_list.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='staff_login')
def adm_communeChiefDetails(request, pk):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        chief_id = pk
        # getting chief
        if get_user_model().objects.filter(is_chief_commune=True, id=chief_id).exists():
            # if exists
            foundData = get_user_model().objects.get(id=chief_id)

            if 'update_chief' in request.POST:
                # Retrieve the form data from the request
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                gender = request.POST.get('gender')
                phone = request.POST.get('phone')
                commune_id = request.POST.get('commune')
                # profilePicture = request.FILES.get('profilePicture')

                if first_name and last_name and email and gender and commune_id:
                    if get_user_model().objects.filter(email=email).exclude(id=chief_id):
                        messages.warning(request, "Email already exist.")
                        return redirect(adm_communeChiefDetails, pk)
                    elif get_user_model().objects.filter(commune=commune_id).exclude(id=chief_id):
                        messages.warning(request, "Commune already assigned to a chief.")
                        return redirect(adm_communeChiefDetails, pk)
                    else:
                        # Update Chief
                        chiefDetails = foundData
                        chiefDetails.first_name = first_name
                        chiefDetails.last_name = last_name
                        chiefDetails.email = email
                        chiefDetails.gender = gender
                        chiefDetails.commune = Commune.objects.get(id=commune_id)
                        chiefDetails.phone = phone
                        chiefDetails.save()
                        
                        messages.success(
                        request, "Chief "+first_name+" "+last_name+", Updated successfully.")
                        return redirect(adm_communeChiefDetails, pk)
                else:
                    messages.error(request, ('Error , All fields are required!'))
                    return redirect(adm_communeChiefDetails, pk)

            elif 'delete_chief' in request.POST:
                # Delete chief
                delete_chief = get_user_model().objects.get(is_chief_commune=True,id=chief_id)
                delete_chief.delete()
                messages.success(request, "Chief Commune info deleted successfully.")
                return redirect(adm_communeChiefs)

            else:
                # request_data = Application.objects.filter(status="Waiting")
                
                # getting commune
                communeData = Commune.objects.filter().order_by('commune_name')
                context = {
                    'title': 'National Administrator - Chief Commune Info',
                    'chief_active': 'active',
                    'chief': foundData,
                    'communes': communeData,
                    # 'request_data': request_data,
                }
                return render(request, 'management/administrator/chiefCommune_details.html', context)
        else:
            messages.error(request, ('Chief not found'))
            return redirect(adm_communeChiefs)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)




@login_required(login_url='staff_login')
def adm_publications(request):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        if 'new_publication' in request.POST:
            title = request.POST.get("title")
            publication_file = request.FILES["publication_file"]

            if title and publication_file:
                found_data = Publication.objects.filter(title=title)
                if found_data:
                    messages.warning(request, "The Publication with title "+title+", Already exist.")
                    return redirect(adm_publications)
                else:
                    # add new publication
                    addPubication = Publication(
                        recorded_by=request.user,
                        title=title,
                        files=publication_file,
                    )
                    addPubication.save()

                    messages.success(
                        request, "New Publication created successfully.")
                    return redirect(adm_publications)
            else:
                messages.error(request, "Error , All fields are required!")
                return redirect(adm_publications)
        else:
            # request_data = Application.objects.filter(status="Waiting")
            # getting publications
            PublicationData = Publication.objects.filter().order_by('publication_date')
            context = {
                'title': 'National Administrator - Publications List',
                'publication_active': 'active',
                'publications': PublicationData,
                # 'request_data': request_data,
            }
            return render(request, 'management/administrator/publication_list.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='staff_login')
def adm_publicationDetails(request, pk):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        publication_id = pk
        # getting publication
        if Publication.objects.filter(id=publication_id).exists():
            # if exists
            foundData = Publication.objects.get(id=publication_id)

            if 'update_publication' in request.POST:
                # Retrieve the form data from the request
                title = request.POST.get("title")

                if title:
                    if Publication.objects.filter(title=title).exclude(id=publication_id):
                        messages.warning(
                            request, "Publication with title "+title+", already exist.")
                        return redirect(adm_publicationDetails, pk)
                    else:
                        # Update publication
                        if 'publication_file' in request.FILES:
                            publication_file = request.FILES["publication_file"]
                            publication_updated = foundData
                            publication_updated.title=title
                            publication_updated.files=publication_file
                        else:
                            publication_updated = foundData
                            publication_updated.title=title
                        
                        publication_updated.save()
                        messages.success(request, "Publication Updated successfully.")
                        return redirect(adm_publicationDetails, pk)
                else:
                    messages.error(request, ('Publication title is required.'))
                    return redirect(adm_publicationDetails, pk)

            elif 'delete_publication' in request.POST:
                # Delete publication
                delete_publication = Publication.objects.get(id=publication_id)
                delete_publication.delete()
                messages.success(request, "Publication info deleted successfully.")
                return redirect(adm_publications)

            else:
                # request_data = Application.objects.filter(status="Waiting")
                
                context = {
                    'title': 'National Administrator - Publication Info',
                    'publication_active': 'active',
                    'publication': foundData,
                    # 'request_data': request_data,
                }
                return render(request, 'management/administrator/publication_details.html', context)
        else:
            messages.error(request, ('Commune not found'))
            return redirect(adm_publications)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)




@login_required(login_url='staff_login')
def adm_citizens(request):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        if 'new_citizen' in request.POST:
            # Retrieve the form data from the request
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            gender=request.POST.get('gender')
            birthdate=request.POST.get('birthdate')
            birth_place=request.POST.get('birth_place')
            volume_no=request.POST.get('volume_no')
            father_fname=request.POST.get('father_fname')
            father_lname=request.POST.get('father_lname')
            mother_fname=request.POST.get('mother_fname')
            mother_lname=request.POST.get('mother_lname')

            if first_name and last_name and gender and birthdate and birth_place and volume_no and father_fname and father_lname and mother_fname and mother_lname:
                if Citizen.objects.filter(volume_number=volume_no):
                    messages.warning(request, "Citizen with volume number "+volume_no+", already exist.")
                    return redirect(adm_citizens)
                else:
                    # add new citizen
                    newCitizen = Citizen.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        gender=gender,
                        birthdate=birthdate,
                        birth_place=Colline.objects.get(id=birth_place),
                        volume_number=volume_no,
                    )
                    if newCitizen:
                        # Create parent records if provided
                        if father_fname and father_lname:
                            CitizenParent.objects.create(
                                citizen=newCitizen,
                                parent=CitizenParent.Parent.FATHER,
                                first_name=father_fname,
                                last_name=father_lname
                            )

                        if mother_fname and mother_lname:
                            CitizenParent.objects.create(
                                citizen=newCitizen,
                                parent=CitizenParent.Parent.MOTHER,
                                first_name=mother_fname,
                                last_name=mother_lname
                            )
                        messages.success(request, "Citizen "+first_name+" "+last_name+", registered successfully.")
                        return redirect(adm_citizens)
                    else:
                        messages.error(request, ('Process Failed.'))
                        return redirect(adm_citizens)
            else:
                messages.error(request, "Error , All fields are required!")
                return redirect(adm_citizens)
        else:
            # getting colline
            CollineData = Colline.objects.filter().order_by('colline_name')
            # getting citizen
            citizensData = Citizen.objects.filter().order_by('birth_place', 'createdDate')
            context = {
                'title': 'National Administrator - Citizens List',
                'citizens_active': 'active',
                'citizens': citizensData,
                'collines': CollineData,
            }
            return render(request, 'management/administrator/citizen_list.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='staff_login')
def adm_citizenDetails(request, pk):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        citizen_id = pk
        # getting citizen
        if Citizen.objects.filter(id=citizen_id).exists():
            # if exists
            foundData = Citizen.objects.get(id=citizen_id)

            if 'update_citizen' in request.POST:
                # Retrieve the form data from the request
                first_name=request.POST.get('first_name')
                last_name=request.POST.get('last_name')
                gender=request.POST.get('gender')
                birthdate=request.POST.get('birthdate')
                birth_place=request.POST.get('birth_place')
                volume_no=request.POST.get('volume_no')


                if first_name and last_name and gender and birthdate and birth_place and volume_no:
                    if Citizen.objects.filter(volume_number=volume_no).exclude(id=citizen_id):
                        messages.warning(request, "Volume number "+volume_no+", already taken.")
                        return redirect(adm_citizenDetails, pk)
                    else:
                        # Update citizen
                        citizenDetails = foundData
                        citizenDetails.first_name=first_name
                        citizenDetails.last_name=last_name
                        citizenDetails.gender=gender
                        citizenDetails.birthdate=birthdate
                        citizenDetails.birth_place=Colline.objects.get(id=birth_place)
                        citizenDetails.volume_number=volume_no
                        citizenDetails.save()
                        
                        messages.success(
                        request, "Citizen "+first_name+" "+last_name+", Updated successfully.")
                        return redirect(adm_citizenDetails, pk)
                else:
                    messages.error(request, ('Error , All fields are required!'))
                    return redirect(adm_citizenDetails, pk)
            
            if 'update_parents' in request.POST:
                # Retrieve the form data from the request
                father_fname=request.POST.get('father_fname')
                father_lname=request.POST.get('father_lname')
                mother_fname=request.POST.get('mother_fname')
                mother_lname=request.POST.get('mother_lname')

                if father_fname and father_lname and mother_fname and mother_lname:
                    # Update or create parent records if provided
                    father = CitizenParent.objects.filter(citizen=foundData, parent=CitizenParent.Parent.FATHER).first()
                    if father:
                        father.first_name = father_fname
                        father.last_name = father_lname
                        father.save()

                    mother = CitizenParent.objects.filter(citizen=foundData, parent=CitizenParent.Parent.MOTHER).first()
                    if mother:
                        mother.first_name = mother_fname
                        mother.last_name = mother_lname
                        mother.save()
                        
                    messages.success(request, "Citizen parents Info Updated successfully.")
                    return redirect(adm_citizenDetails, pk)
                else:
                    messages.error(request, ('Error , All fields are required!'))
                    return redirect(adm_citizenDetails, pk)

            elif 'delete_citizen' in request.POST:
                # Delete citizen
                delete_chief = foundData
                delete_chief.delete()
                messages.success(request, "Citizen info deleted successfully.")
                return redirect(adm_citizens)

            else:
                # getting colline
                CollineData = Colline.objects.filter().order_by('colline_name')
                context = {
                    'title': 'National Administrator - Citizen Info',
                    'citizens_active': 'active',
                    'citizen': foundData,
                    'collines': CollineData,
                }
                return render(request, 'management/administrator/citizen_details.html', context)
        else:
            messages.error(request, ('Citizen not found'))
            return redirect(adm_citizens)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='staff_login')
def adm_nidApplications_list(request):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        # getting nid application
        applicationsData = IDCardRegistration.objects.filter().order_by('status','registration_date')
        context = {
            'title': 'NID Applications List',
            'nidApplication_active': 'active',
            'nid_applications': applicationsData,
        }
        return render(request, 'management/administrator/nid_applicationList.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='staff_login')
def adm_nidApplicationDetail(request, pk):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        application_id = pk
        # getting nid application
        if IDCardRegistration.objects.filter(id=application_id).exists():
            # if exists
            foundData = IDCardRegistration.objects.get(id=application_id)

            context = {
                'title': 'NID application details',
                'nidApplication_active': 'active',
                'data': foundData,
            }
            return render(request, 'management/administrator/nid_applicationDetails.html', context)
        else:
            messages.error(request, ('NID Application not found'))
            return redirect(adm_nidApplications_list)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='staff_login')
def adm_lostNID_report(request):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        # getting nid lost reports
        reportsData = LostIDCardReport.objects.filter().order_by('created_date')
        context = {
            'title': 'Lost NID Report',
            'lost_nid_active': 'active',
            'lost_nid_reports': reportsData,
        }
        return render(request, 'management/administrator/lost_nidReportList.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='staff_login')
def adm_NID_reportDetail(request, pk):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        report_id = pk
        # getting report
        if LostIDCardReport.objects.filter(id=report_id).exists():
            # if exists
            foundData = LostIDCardReport.objects.get(id=report_id)
            
            context = {
                'title': 'Lost NID Report details',
                'lost_nid_active': 'active',
                'report': foundData,
            }
            return render(request, 'management/administrator/lost_nidReportDetails.html', context)
        else:
            messages.error(request, ('Data not found'))
            return redirect(adm_lostNID_report)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)




@login_required(login_url='staff_login')
def adm_registeredNID_list(request):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        # getting nid application
        registered_nid = RegisteredIDCard.objects.filter().order_by('created_date')
        context = {
            'title': 'Registered NID List',
            'registered_nid_active': 'active',
            'registered_nid': registered_nid,
        }
        return render(request, 'management/administrator/registered_nidList.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='staff_login')
def adm_registeredNIDCardDetails(request, pk):
    if request.user.is_authenticated and request.user.is_nationalAdministrator == True:
        # getting registered nid data
        if RegisteredIDCard.objects.filter(id=pk).exists():
            # if exists
            foundData = RegisteredIDCard.objects.get(id=pk)
            
            context = {
                'title': 'Registered NID Card Details',
                'registered_nid_active': 'active',
                'data': foundData,
            }
            return render(request, 'management/administrator/registered_nidCardDetails.html', context)
        else:
            messages.error(request, ('Data not found'))
            return redirect(adm_registeredNID_list)
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
            'title': 'Dashboard',
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
                'title': 'My Profile',
            }
            return render(request, 'management/commune/profile.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='staff_login')
def chief_services(request):
    if request.user.is_authenticated and request.user.is_chief_commune == True:
        # request_data = Application.objects.filter(status="Waiting")
        # getting services
        ServiceData = Service.objects.filter().order_by('service_name')
        context = {
            'title': 'Service List',
            'service_active': 'active',
            'services': ServiceData,
            # 'request_data': request_data,
        }
        return render(request, 'management/commune/service_list.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)




@login_required(login_url='staff_login')
def chief_citizens(request):
    if request.user.is_authenticated and request.user.is_chief_commune == True:
        if 'new_citizen' in request.POST:
            # Retrieve the form data from the request
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            gender=request.POST.get('gender')
            birthdate=request.POST.get('birthdate')
            birth_place=request.POST.get('birth_place')
            volume_no=request.POST.get('volume_no')
            father_fname=request.POST.get('father_fname')
            father_lname=request.POST.get('father_lname')
            mother_fname=request.POST.get('mother_fname')
            mother_lname=request.POST.get('mother_lname')

            if first_name and last_name and gender and birthdate and birth_place and volume_no and father_fname and father_lname and mother_fname and mother_lname:
                if Citizen.objects.filter(volume_number=volume_no):
                    messages.warning(request, "Citizen with volume number "+volume_no+", already exist.")
                    return redirect(chief_citizens)
                else:
                    # add new citizen
                    newCitizen = Citizen.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        gender=gender,
                        birthdate=birthdate,
                        birth_place=Colline.objects.get(id=birth_place),
                        volume_number=volume_no,
                    )
                    if newCitizen:
                        # Create parent records if provided
                        if father_fname and father_lname:
                            CitizenParent.objects.create(
                                citizen=newCitizen,
                                parent=CitizenParent.Parent.FATHER,
                                first_name=father_fname,
                                last_name=father_lname
                            )

                        if mother_fname and mother_lname:
                            CitizenParent.objects.create(
                                citizen=newCitizen,
                                parent=CitizenParent.Parent.MOTHER,
                                first_name=mother_fname,
                                last_name=mother_lname
                            )
                        messages.success(request, "Citizen "+first_name+" "+last_name+", registered successfully.")
                        return redirect(chief_citizens)
                    else:
                        messages.error(request, ('Process Failed.'))
                        return redirect(chief_citizens)
            else:
                messages.error(request, "Error , All fields are required!")
                return redirect(chief_citizens)
        else:
            # getting colline
            CollineData = Colline.objects.filter(commune=request.user.commune).order_by('colline_name')
            # getting citizen
            citizensData = Citizen.objects.filter(birth_place__commune=request.user.commune).order_by('birth_place', 'createdDate')
            context = {
                'title': str(request.user.commune)+' Citizens',
                'citizens_active': 'active',
                'citizens': citizensData,
                'collines': CollineData,
            }
            return render(request, 'management/commune/citizen_list.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='staff_login')
def chief_citizenDetails(request, pk):
    if request.user.is_authenticated and request.user.is_chief_commune == True:
        citizen_id = pk
        # getting citizen
        if Citizen.objects.filter(birth_place__commune=request.user.commune, id=citizen_id).exists():
            # if exists
            foundData = Citizen.objects.get(birth_place__commune=request.user.commune, id=citizen_id)

            # getting colline
            CollineData = Colline.objects.filter(commune=request.user.commune).order_by('colline_name')
            context = {
                'title': 'Citizen Info',
                'citizens_active': 'active',
                'citizen': foundData,
                'collines': CollineData,
            }
            return render(request, 'management/commune/citizen_details.html', context)
        else:
            messages.error(request, ('Citizen not found'))
            return redirect(chief_citizens)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='staff_login')
def chief_nidApplications_list(request):
    if request.user.is_authenticated and request.user.is_chief_commune == True:
        if 'verify_citizen' in request.POST:
            # Retrieve the form data from the request
            volume_no=request.POST.get('volume_no')

            if volume_no:
                if not Citizen.objects.filter(volume_number=volume_no).exists():
                    messages.warning(request, "Invalid volume number!")
                    return redirect(chief_nidApplications_list)
                else:
                    request.session['valid_applicant'] = Citizen.objects.get(
                        volume_number=volume_no).id
                    return redirect(chief_nidApplication)
            else:
                messages.error(
                    request, "Error , Citizen volume number is required!")
                return redirect(chief_nidApplications_list)
        else:
            # getting nid application
            applicationsData = IDCardRegistration.objects.filter(recorded_by=request.user, status="Waiting").order_by('registration_date')
            context = {
                'title': 'NID Applications List',
                'nidApplication_active': 'active',
                'nid_applications': applicationsData,
            }
            return render(request, 'management/commune/nid_applicationList.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='staff_login')
def chief_nidApplication(request):
    if request.user.is_authenticated and request.user.is_chief_commune == True:
        # get applicant
        valid_applicant = request.session.get('valid_applicant')
        if valid_applicant:
            # getting citizen data
            citizenData = Citizen.objects.get(id=valid_applicant)
            if request.method == 'POST':
                resident_address = request.POST.get('resident_address')
                picture = request.FILES['picture']
                email = request.POST.get('email')

                if not (resident_address and picture and email):
                    messages.warning(request, "Error , All fields are required.")
                    return redirect(chief_nidApplication)
                else:
                    # record new nid application
                    nidApplication = IDCardRegistration(
                        citizen=citizenData,
                        email=email,
                        resident_address=Commune.objects.get(id=resident_address),
                        picture=picture,
                        recorded_by=request.user,
                    )
                    nidApplication.save()

                    messages.success(request, "NID Application has been submitted successfully.")

                    # delete applicant session
                    del request.session['valid_applicant']
                    
                    return redirect(chief_nidApplications_list)
            else:
                # getting commune
                communeData = Commune.objects.filter().order_by('commune_name')
                context = {
                    'title': 'NID Application',
                    'nidApplication_active': 'active',
                    'citizen': citizenData,
                    'communes': communeData,
                }
                return render(request, 'management/commune/nid_application.html', context)
        else:
            return redirect(chief_nidApplications_list)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='staff_login')
def chief_nidApplicationDetail(request, pk):
    if request.user.is_authenticated and request.user.is_chief_commune == True:
        application_id = pk
        # getting nid application
        if IDCardRegistration.objects.filter(recorded_by=request.user, id=application_id).exists():
            # if exists
            foundData = IDCardRegistration.objects.get(id=application_id)

            context = {
                'title': 'NID application details',
                'nidApplication_active': 'active',
                'data': foundData,
            }
            return render(request, 'management/commune/nid_applicationDetails.html', context)
        else:
            messages.error(request, ('NID Application not found'))
            return redirect(chief_nidApplications_list)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)





@login_required(login_url='staff_login')
def chief_lostNID_report(request):
    if request.user.is_authenticated and request.user.is_chief_commune == True:
        if 'verify_citizen' in request.POST:
            # Retrieve the form data from the request
            nid_number=request.POST.get('nid_number')

            if nid_number:
                if not Citizen.objects.filter(nid_number=nid_number).exists():
                    messages.warning(request, "Invalid NID Card number!")
                    return redirect(chief_lostNID_report)
                else:
                    request.session['valid_applicant'] = Citizen.objects.get(nid_number=nid_number).id
                    return redirect(chief_newLostNID_report)
            else:
                messages.error(
                    request, "Error , Citizen NID Card number is required!")
                return redirect(chief_lostNID_report)
        else:
            # getting nid lost reports
            reportsData = LostIDCardReport.objects.filter(recorded_by=request.user).order_by('created_date')
            context = {
                'title': 'Lost NID Report',
                'lost_nid_active': 'active',
                'lost_nid_reports': reportsData,
            }
            return render(request, 'management/commune/lost_nidList.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='staff_login')
def chief_newLostNID_report(request):
    if request.user.is_authenticated and request.user.is_chief_commune == True:
        # get applicant
        valid_applicant = request.session.get('valid_applicant')
        if valid_applicant:
            # getting citizen data
            citizenData = Citizen.objects.get(id=valid_applicant)
            if request.method == 'POST':
                date_lost = request.POST.get('date_lost')
                description = request.POST.get('description')
                email = request.POST.get('email')
                contact_info = request.POST.get('contact_info')

                if not (date_lost and description and contact_info and email):
                    messages.warning(request, "Error , All fields are required.")
                    return redirect(chief_newLostNID_report)
                else:
                    # record lost nid report
                    lostNID = LostIDCardReport(
                        citizen=citizenData,
                        card_number=citizenData.nid_number,
                        email=email,
                        contact_info=contact_info,
                        description=description,
                        date_lost=date_lost,
                        recorded_by=request.user,
                    )
                    lostNID.save()

                    messages.success(request, "Lost NID Report has been submitted successfully.")

                    # delete applicant session
                    del request.session['valid_applicant']
                    
                    return redirect(chief_lostNID_report)
            else:
                context = {
                    'title': 'Lost NID Report',
                    'lost_nid_active': 'active',
                    'citizen': citizenData,
                }
                return render(request, 'management/commune/lost_nidReport.html', context)
        else:
            return redirect(chief_lostNID_report)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='staff_login')
def chief_NID_reportDetail(request, pk):
    if request.user.is_authenticated and request.user.is_chief_commune == True:
        report_id = pk
        # getting report
        if LostIDCardReport.objects.filter(recorded_by=request.user, id=report_id).exists():
            # if exists
            foundData = LostIDCardReport.objects.get(id=report_id)
            
            context = {
                'title': 'Lost NID Report details',
                'lost_nid_active': 'active',
                'report': foundData,
            }
            return render(request, 'management/commune/lost_nidReportDetails.html', context)
        else:
            messages.error(request, ('Data not found'))
            return redirect(chief_lostNID_report)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)




@login_required(login_url='staff_login')
def chief_registeredNID_list(request):
    if request.user.is_authenticated and request.user.is_chief_commune == True:
        # getting nid application
        registered_nid = RegisteredIDCard.objects.filter(placeofissue=request.user.commune).exclude(is_taken=True).order_by('created_date')
        context = {
            'title': 'Registered NID List',
            'registered_nid_active': 'active',
            'registered_nid': registered_nid,
        }
        return render(request, 'management/commune/registered_nidList.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)



@login_required(login_url='staff_login')
def chief_NID_recievedConfirm(request, pk):
    if request.user.is_authenticated and request.user.is_chief_commune == True:
        # getting registered nid data
        if RegisteredIDCard.objects.filter(placeofissue=request.user.commune, id=pk).exists():
            # if exists
            foundData = RegisteredIDCard.objects.get(id=pk)
            
            if 'confirm' in request.POST:
                # confirm that citizen recieved nid card
                foundData.is_taken=True
                foundData.taken_date=timezone.now()
                foundData.save()
                        
                messages.success(
                request, "Confirmed successfully.")
                return redirect(chief_registeredNID_list)
            else:
                context = {
                    'title': 'NID Recieved Confirm',
                    'registered_nid_active': 'active',
                    'data': foundData,
                }
                return render(request, 'management/commune/nid_recievedConfirm.html', context)
        else:
            messages.error(request, ('Data not found'))
            return redirect(chief_registeredNID_list)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)
