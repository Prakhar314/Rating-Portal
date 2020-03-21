from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm 
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.
def register(request):
    if request.method =='POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            print(username)
            messages.success(request,f'Account created for {username}')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request,'users/register.html',{'form': form})

def homeView(request):
    return render(request,'users/homepage.html')

@login_required
def profile(request):
    return render(request,'users/profile.html')

def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'An error occurred.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/changePass.html', {'form': form})