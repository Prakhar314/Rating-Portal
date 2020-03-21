from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm 
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
    return render(request,'users/register.html',{'title':'Register','form': form})

def homeView(request):
    return render(request,'users/homepage.html',{'title':'Home'})

@login_required
def profile(request):
    return render(request,'users/profile.html',{'title':'User Profile'})