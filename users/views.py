from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime,timedelta
import pytz

from .forms import UserRegistrationForm 
from .forms import BanForm
from review.models import Review
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
def profile(request,profileOwner):
    #print(type())
    return render(request,'users/profile.html',{'profileOwner':User.objects.get(username=profileOwner)})
    
@login_required
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

@login_required
def banView(request, userID, reviewID):
    user = User.objects.get(id=userID)
    review =Review.objects.get(id=reviewID)
    context={}
    context['next']=request.build_absolute_uri(request.GET["next"])
    context['review']=review
    #print(context['next'])
    nextYes='/issues/'
    if request.user.is_superuser:
        if request.method=='POST':
            form = BanForm(request.POST)
            context['form']=form
            if form.is_valid():
                customUserModel=user.customusermodel
                banDays=form.cleaned_data.get('banDays')
                if banDays==-1:
                    user.delete()
                else:
                    customUserModel.bannedTill = datetime.now(pytz.utc)+timedelta(days=form.cleaned_data.get('banDays'))
                    customUserModel.save()
                    review.delete()
                return redirect(nextYes)
        else:
            form = BanForm()
            context['form']=form
        return render(request, 'users/ban.html', context)
    else:
        return Http404
