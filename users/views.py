from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime, timedelta
import pytz

from .forms import UserRegistrationForm
from .forms import BanForm
from review.models import *

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            print(username)
            messages.success(request, f"Account created for {username}")
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, "users/register.html", {"form": form})


def homeView(request):
    return render(request, "users/homepage.html")


@login_required
def profile(request, profileOwner):
    profileOwner=User.objects.get(username=profileOwner)
    # print(type())
    if request.method == "POST":
        postValues=dict(request.POST).values()
        if ['Like'] in postValues or['Liked'] in postValues:
            for key, value in dict(request.POST).items(): 
                if ['Like'] == value or ['Liked'] == value: 
                    break
            review = Review.objects.get(id=int(key.split('-')[1]))
            actionLink=request.build_absolute_uri(f'/profile/{review.author.username}')
            reviewAuthor=review.author.username
            if review.isAnonymous and not request.user.is_superuser:
                actionLink=None
                reviewAuthor='Anonymous'
            try:
                review.likes
            except Review.likes.RelatedObjectDoesNotExist as identifier:
                Like.objects.create(review=review)
            try:
                review.dislikes
            except Review.dislikes.RelatedObjectDoesNotExist as identifier:
                Dislike.objects.create(review=review)
            if request.user not in review.likes.users.all():
                review.likes.users.add(request.user)
                RecentAction.create(request.user,f'You liked {reviewAuthor}\'s review','i',actionLink).save()
                if request.user in review.dislikes.users.all():
                    review.dislikes.users.remove(request.user)
            else:
                RecentAction.create(request.user,f'You removed your like from {reviewAuthor}\'s review','i',actionLink).save()
                review.likes.users.remove(request.user)
                #print('like',list(review.likes.users.all()))
                #print('dislike',list(review.dislikes.users.all()))
        elif  ['Dislike'] in postValues or ['Disliked'] in postValues:
            for key, value in dict(request.POST).items(): 
                if ['Dislike'] == value or ['Disliked'] == value: 
                    break
            review = Review.objects.get(id=int(key.split('-')[1]))
            actionLink=request.build_absolute_uri(f'/profile/{review.author.username}')
            reviewAuthor=review.author.username
            if review.isAnonymous and not request.user.is_superuser:
                actionLink=None
                reviewAuthor='Anonymous'
            try:
                review.likes
            except Review.likes.RelatedObjectDoesNotExist as identifier:
                Like.objects.create(review=review)
            try:
                review.dislikes
            except Review.dislikes.RelatedObjectDoesNotExist as identifier:
                Dislike.objects.create(review=review)
            if request.user not in review.dislikes.users.all():
                RecentAction.create(request.user,f'You disliked {reviewAuthor}\'s review','i',actionLink).save()
                review.dislikes.users.add(request.user)
                if request.user in review.likes.users.all():
                    review.likes.users.remove(request.user)
            else:
                RecentAction.create(request.user,f'You removed your dislike from {reviewAuthor}\'s review','i',actionLink).save()
                review.dislikes.users.remove(request.user)
                #print('like',list(review.likes.users.all()))
                #print('dislike',list(review.dislikes.users.all()))
    return render(
        request,
        "users/profile.html",
        {"profileOwner": profileOwner,'currentView':'profile','profileScore':profileOwner.customusermodel.getTotalScore()},
    )


@login_required
def changePassword(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Password was successfully updated!")
            return redirect("home")
        else:
            messages.error(request, "An error occurred.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "users/changePass.html", {"form": form})


@login_required
def banView(request, userID, reviewID):
    user = User.objects.get(id=userID)
    review = Review.objects.get(id=reviewID)
    context = {}
    context["next"] = request.build_absolute_uri(request.GET["next"])
    context["review"] = review
    context['alreadyBanned']=None
    if user.customusermodel.bannedTill>datetime.now(pytz.utc):
        context['alreadyBanned'] = user.customusermodel.bannedTill
    # print(context['next'])
    nextYes = "/issues/"
    if request.user.is_superuser:
        if request.method == "POST":
            form = BanForm(request.POST)
            context["form"] = form
            if form.is_valid():
                customUserModel = user.customusermodel
                banDays = form.cleaned_data.get("banDays")
                actionLink=None
                if banDays == -1:
                    actionDetail=f'You removed {review.author.username}.'
                    user.delete()
                else:
                    actionDetail=f'You banned {review.author.username} for {banDays} day(s).'
                    actionLink=request.build_absolute_uri(f'/profile/{review.author.username}') 
                    customUserModel.bannedTill = datetime.now(pytz.utc) + timedelta(
                        days=form.cleaned_data.get("banDays")
                    )
                    rc= RecentAction.create(review.author,f'You have been banned for {banDays} day(s)','a',None)
                    rc.save()
                    customUserModel.save()
                    review.delete()

                actionType='a'
                rca= RecentAction.create(request.user,actionDetail,actionType,actionLink)
                rca.save()

                return redirect(nextYes)
        else:
            form = BanForm()
            context["form"] = form
        return render(request, "users/ban.html", context)
    else:
        return Http404
