from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Review
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def deleteReview(request,reviewID,type):
    review = Review.objects.get(id=reviewID)
    if type=='from_profile':
        next=['profile',request.user.username]
    else:
        next=['course',review.courseName]
    if review.author == request.user:
        if request.method == "POST":
            messages.success(request,'Review Deleted')
            review.delete()
            return HttpResponseRedirect(reverse(next[0],args=(next[1],)))
        else:
            return render(request,'review/delete.html',{'review':review,'type':type})
    else:
        raise Http404
