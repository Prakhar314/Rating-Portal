from django.shortcuts import render
from django.apps import apps
from django.http import Http404

def courseView(request,courseName):
    reviews,rating = recheckRatingsFor(courseName)
    courseList= getAllOf('courses')
    if courseName not in [c.courseName for c in courseList]:
        raise Http404('No such Course')
    return render(request,'courses/coursePage.html',{'reviews':reviews,'courseName':courseName,'rating':rating})

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