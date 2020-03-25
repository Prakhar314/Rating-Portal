from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Review, Report
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from .forms import ReportForm


@login_required
def deleteReview(request, reviewID):
    review = Review.objects.get(id=reviewID)
    nextURI=request.GET["next"]
    if str(nextURI).startswith('reportAction'):
        nextNo=request.build_absolute_uri(nextURI[12:])
        nextYes='/issues/'
    else:
        nextYes=nextNo=request.build_absolute_uri(nextURI)
    if (review.author == request.user) or request.user.is_superuser:
        if request.method == "POST":
            messages.success(request, "Review Deleted")
            review.delete()
            return redirect(nextYes)
        else:
            return render(
                request, "review/delete.html", {"review": review, "next": nextNo,"choiceQuestion" : "Do you want to delete this review?"}
            )
    else:
        raise Http404

@login_required
def ignoreReports(request, reviewID):
    review = Review.objects.get(id=reviewID)
    reports = list(review.flags.all())
    nextURI=request.GET["next"]
    if str(nextURI).startswith('reportAction'):
        nextNo=request.build_absolute_uri(nextURI[12:])
        nextYes='/issues/'
    else:
        nextYes=nextNo=request.build_absolute_uri(nextURI)
    if request.user.is_superuser:
        if request.method == "POST":
            messages.success(request, "Reports Ignored")
            for report in reports:
                report.delete()
            return redirect(nextYes)
        else:
            return render(
                request, "review/delete.html", {"review": review, "next": nextNo, "choiceQuestion" : "Do you want to ignore reports for this?"}
            )
    else:
        raise Http404


@login_required
def reportFormView(request, reviewID):
    review = Review.objects.get(id=reviewID)
    next = request.build_absolute_uri(request.GET["next"])
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=True)
            report.reviewReported = review
            report.save()
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
