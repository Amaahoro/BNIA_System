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

