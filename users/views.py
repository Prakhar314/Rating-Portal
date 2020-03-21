from django.shortcuts import render,redirect
from django.contrib import messages
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
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request,'users/register.html',{'title':'Register','form': form})

def homeView(request):
    return render(request,'users/homepage.html',{'title':'Home'})