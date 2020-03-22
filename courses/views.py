from django.shortcuts import render,redirect
from django.apps import apps
from django.http import Http404
from review.forms import CommentForm

def courseView(request,courseName):
    reviews,rating = recheckRatingsFor(courseName)
    courseList= getAllOf('courses')

    if courseName not in [c.courseName for c in courseList]:
        raise Http404('No such Course')

    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=True)
            new_comment.author = request.user
            new_comment.courseName=courseName
            new_comment.save()
            return redirect('course',courseName=courseName)
    else:
        comment_form = CommentForm()

    return render(request,'courses/coursePage.html',{'reviews':reviews,'courseName':courseName,'rating':rating,'commentForm':comment_form})

def courseListView(request):
    recheckAllRatings()
    courseList = getAllOf('courses')
    return render(request,'courses/courseList.html',{'list':courseList})

def recheckRatingsFor(courseName):
    reviews = getAllOf('review')
    reviews = list(filter(lambda x:x.courseName==courseName,reviews))
    if len(reviews)==0:
        return [],'Unrated'
    rating = round(sum(x.score for x in reviews)/len(reviews),2)
    return reviews,rating

def recheckAllRatings():
    courseList = getAllOf('courses')
    reviews = getAllOf('review')
    results={}
    for review in reviews:
        try:
            results[review.courseName][0]+=review.score
            results[review.courseName][1]+=1
        except:
            results[review.courseName]=[review.score,1]
    for course in courseList:
        try:
            result=results[course.courseName]
        except:
            course.rating = -1
            course.noOfReviews = 0
            course.save()
            continue
        course.rating = round(result[0]/result[1],2)
        course.noOfReviews = result[1]
        course.save()

def getAllOf(name):
    for r in apps.get_app_config(name).get_models():
        objects = list(r.objects.all())
    return objects