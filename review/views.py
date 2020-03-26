from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from .forms import ReportForm


@login_required
def deleteReview(request, reviewID):
    review = Review.objects.get(id=reviewID)
    nextURI = request.GET["next"]
    if str(nextURI).startswith("reportAction"):
        nextNo = request.build_absolute_uri(nextURI[12:])
        nextYes = "/issues/"
    else:
        nextYes = nextNo = request.build_absolute_uri(nextURI)
    if (review.author == request.user) or request.user.is_superuser:
        if request.method == "POST":
            actionDetail=f'You deleted your review on {review.courseName}'
            actionType='i'
            if review.author != request.user:
                actionDetail=f'Your review on {review.courseName} was removed by admin'
                actionType='a'
                rca= RecentAction.create(request.user,f'You deleted {review.author.username}\'s review',actionType,request.build_absolute_uri(f'/profile/{review.author.username}') )
                rca.save()
                rc= RecentAction.create(review.author,'You have been warned for your recent actions',actionType,None)
                rc.save()
            rc= RecentAction.create(review.author,actionDetail,actionType,None)
            rc.save()
            review.delete()
            messages.success(request, "Review Deleted")
            return redirect(nextYes)
        else:
            return render(
                request,
                "review/delete.html",
                {
                    "review": review,
                    "next": nextNo,
                    "choiceQuestion": "Do you want to delete this review?",
                },
            )
    else:
        raise Http404


@login_required
def ignoreReports(request, reviewID):
    review = Review.objects.get(id=reviewID)
    reports = list(review.flags.all())
    nextURI = request.GET["next"]
    if str(nextURI).startswith("reportAction"):
        nextNo = request.build_absolute_uri(nextURI[12:])
        nextYes = "/issues/"
    else:
        nextYes = nextNo = request.build_absolute_uri(nextURI)
    if request.user.is_superuser:
        if request.method == "POST":

            actionDetail=f'You removed reports against {review.author.username}'
            actionType='i'
            rca= RecentAction.create(request.user,actionDetail,actionType,request.build_absolute_uri(f'/profile/{review.author.username}') )
            rca.save()

            messages.success(request, "Reports Ignored")
            for report in reports:
                report.delete()
            return redirect(nextYes)
        else:
            return render(
                request,
                "review/delete.html",
                {
                    "review": review,
                    "next": nextNo,
                    "choiceQuestion": "Do you want to ignore reports for this?",
                },
            )
    else:
        raise Http404


@login_required
def reportFormView(request, reviewID):
    review = Review.objects.get(id=reviewID)
    if request.user.username in review.flaggers():
        return Http404
    next = request.build_absolute_uri(request.GET["next"])
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=True)
            report.reviewReported = review
            report.reporter = request.user.username
            report.save()

            actionDetail=f'You made a report against {review.author.username}\'s review'
            actionType='i'
            rc= RecentAction.create(request.user,actionDetail,actionType,request.build_absolute_uri(f'/profile/{review.author.username}') )
            rc.save()

            messages.success(request, "Review Reported")
            return redirect(next)
        else:
            messages.error(request, "An error occurred.")
    else:
        form = ReportForm()
    return render(
        request, "review/report.html", {"form": form, "review": review, "next": next}
    )


@login_required
def issueView(request):
    if not request.user.is_superuser:
        raise Http404("Not found")
    reports = list(Report.objects.all())
    reviewList = []
    for report in reports:
        if report.reviewReported not in reviewList:
            reviewList.append(report.reviewReported)
    return render(request, "review/issues.html", {"reviewList": list(reviewList)})


@login_required
def adminReportAction(request, reviewID):
    if request.user.is_superuser:
        return render(
            request,
            "review/adminReportAction.html",
            {"review": Review.objects.get(id=reviewID)},
        )
