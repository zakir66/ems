from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from ems.decorators import admin_only
from .models import Profile
from .forms import UserForm
# Create your views here.


def user_login(request):
    context = {

    }
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if request.GET.get('next', None):
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            context={
                'error':"Your password or username incorrect!"
            }
            return render(request, "auth/login.html", context)
    else:
        return render(request, "auth/login.html", context)

@login_required(login_url="/login/")
def success(request):
    user = request.user
    context = {
        'user':user
    }
    return render(request, 'auth/success.html', context)

def user_logout(request):
    if request.method == "POST":
        logout(request)
        return HttpResponseRedirect(reverse('user_login'))

@login_required(login_url="/login/")
def employee_list(request):
    users = User.objects.all()
    # groups = request.user.groups.all()
    # if groups:
    #     role = groups[0].name
    # if role == "HR":
    print(request.role)

    context = {
        'title':"Employee",
        'users':users
    }
    return render(request, 'employee/index.html', context)

@login_required(login_url="/login/")
def employee_details(request, id=None):
    user = get_object_or_404(User, id=id)
    profile = get_object_or_404(Profile, id=id)
    context={
        'user':user,
        'profile':profile
    }
    return render(request, 'employee/details.html', context)

@login_required(login_url="/login/")
#@role_required(allowed_roles=["Admin", "HR"])
@admin_only
def employee_add(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        context ={
            'user_form':user_form
        }
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request, 'employee/add.html', context)
    else:
        user_form=UserForm()
        context = {
            'user_form': user_form
        }
        return render(request, 'employee/add.html', context)

@login_required(login_url="/login/")
def employee_edit(request, id=None):
    user = get_object_or_404(User, id=id)
    if request.method == "POST":
        user_form=UserForm(request.POST, instance=user)
        context={
            'user_form':user_form
        }
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request, 'employee/edit.html', context)
    else:
        user_form=UserForm(instance=user)
        context={
            'user_form':user_form
        }
        return render(request, 'employee/edit.html', context)

@login_required(login_url="/login/")
def employee_delete(request, id=None):
    user = get_object_or_404(User, id = id)
    if request.method == "POST":
        user.delete()
        return HttpResponseRedirect(reverse('employee_list'))
    else:
        context = {
            'user':user
        }
        return render(request, 'employee/delete.html', context)



# class based view

class ProfileUpdate(UpdateView):
    fields = ['designation', 'salary']
    template_name = 'auth/profile_update.html'
    success_url = reverse_lazy('my_profile')
    def get_object(self):
        return self.request.user.profile

class MyProfile(DetailView):
    template_name = 'auth/profile.html'

    def get_object(self):
        return self.request.user.profile