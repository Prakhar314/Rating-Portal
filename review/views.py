from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Review,Report
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from .forms import ReportForm

@login_required
def deleteReview(request,reviewID,type):
    review = Review.objects.get(id=reviewID)
    if type=='from_profile':
        next=['profile',request.user.username]
    else:
        next=['course',review.courseName]
    if (review.author == request.user) or request.user.is_superuser:
        if request.method == "POST":
            messages.success(request,'Review Deleted')
            review.delete()
            return HttpResponseRedirect(reverse(next[0],args=(next[1],)))
        else:
            return render(request,'review/delete.html',{'review':review,'type':type})
    else:
        raise Http404

def reportFormView(request,reviewID):
    review= Review.objects.get(id=reviewID)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=True)
            report.reviewReported = review
            report.save()
            messages.success(request, 'Review Reported')
            return redirect('home')
        else:
            messages.error(request, 'An error occurred.')
    else:
        form = ReportForm()
    return render(request, 'review/report.html', {'form': form,'review':review})

def issueView(request):
    if not request.user.is_superuser:
        raise Http404('Not found')
    reports = list(Report.objects.all())
    reviewList=[reports[0].reviewReported,]
    for report in reports:
        if report.reviewReported not in reviewList:
            reviewList.append(report.reviewReported)
    return render(request, 'review/issues.html', {'reviewList':list(reviewList)})