from django.shortcuts import render
from django.apps import apps
def courseView(request,courseName):
    reviews,rating = recheckRatingsFor(courseName)
    return render(request,'courses/coursePage.html',{'reviews':reviews,'courseName':courseName,'rating':rating})

def courseListView(request):
    recheckAllRatings()
    for r in apps.get_app_config('courses').get_models():
        courseList = r.objects.all()
    return render(request,'courses/courseList.html',{'list':list(courseList)})

def recheckRatingsFor(courseName):
    for r in apps.get_app_config('review').get_models():
        reviews = r.objects.all()
    reviews = list(filter(lambda x:x.courseName==courseName,reviews))
    if len(reviews)==0:
        return [],'Unrated'
    rating = round(sum(x.score for x in reviews)/len(reviews),2)
    return reviews,rating

def recheckAllRatings():
    for r in apps.get_app_config('courses').get_models():
        courseList = list(r.objects.all())
    for r in apps.get_app_config('review').get_models():
        reviews = list(r.objects.all())
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

