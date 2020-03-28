from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.apps import apps
from django.http import Http404
from django.template.defaultfilters import slugify

from review.forms import CommentForm
from courses.models import Course
from review.models import Review,Like,Dislike,RecentAction
from .forms import CourseForm 


def courseView(request, courseID):
    course = Course.objects.get(id=courseID)
    courseName = course.courseName
    reviews, rating = recheckRatingsFor(courseName)
    courseList = list(Course.objects.all())

    if courseID not in [c.id for c in courseList]:
        raise Http404("No such Course")

    new_comment = None
    comment_form = CommentForm(initial={"author": request.user})
    if request.method == "POST" and request.user.is_authenticated:
        postValues=dict(request.POST).values()
        #print(postValues)
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
        else:
            comment_form = CommentForm(data=request.POST, initial={"author": request.user})
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.author = request.user
                new_comment.courseName = courseName
                new_comment.courseID = courseID
                new_comment.save()
                actionLink=request.build_absolute_uri(f'/course/{courseID}')
                if course.pageType=='p':
                    actionLink=request.build_absolute_uri(f'/professor/{courseID}')
                RecentAction.create(request.user,f'You made a review for {courseName}','i',actionLink).save()
                messages.success(request, "Review submitted")
                return redirect("course", courseID=courseID)

    return render(
        request,
        "courses/coursePage.html",
        {
            "reviews": reviews,
            "courseName": course.courseName,
            "courseDescription": course.courseDescription,
            "rating": rating,
            "commentForm": comment_form,
            'currentView':'course',
        },
    )


def courseListView(request,pageType):
    recheckAllRatings()
    context={}
    allPages=getAllOf(pageType)
    #print(allPages,pageType)
    context['list'] = allPages
    context['pageType'] = pageType.capitalize()
    if request.method=='GET':
        query=request.GET.get('q')
        #print(query)
        if query:
            context['list'] = getCourseFromQuery(str(query),pageType)

    return render(request, "courses/courseList.html", context)

def courseFormView(request):
    if not request.user.is_superuser:
        return Http404
    if request.method == "POST":
        form = CourseForm(data=request.POST)
        if form.is_valid():
            course = form.save(commit=True)
            course.rating=0
            course.noOfReviews=0
            course.save()
            RecentAction.create(request.user,f'You created a page for {course.courseName}','i',request.build_absolute_uri(f'/course/{course.id}')).save()
            if course.pageType=='c':
                messages.success(request,'New Course Created')
                return redirect('/course/')
            elif course.pageType=='p':
                messages.success(request,'New Professor page created')
                return redirect('/professor/')
    else:
        form = CourseForm()
    
    return render(request,'courses/newCourse.html',{'form':form})


def recheckRatingsFor(courseName):
    reviews = getAllOf("review")
    reviews = list(filter(lambda x: x.courseName == courseName, reviews))
    if len(reviews) == 0:
        return [], "Unrated"
    rating = round(sum(x.score for x in reviews) / len(reviews), 2)
    return reviews, rating


def recheckAllRatings():
    courseList = Course.objects.all()
    reviews = getAllOf("review")
    results = {}
    for review in reviews:
        try:
            results[review.courseName][0] += review.score
            results[review.courseName][1] += 1
        except:
            results[review.courseName] = [review.score, 1]
    for course in courseList:
        try:
            result = results[course.courseName]
        except:
            course.rating = -1
            course.noOfReviews = 0
            course.save()
            continue
        course.rating = round(result[0] / result[1], 2)
        course.noOfReviews = result[1]
        course.save()


def getAllOf(name):
    if name == "review":
        return Review.objects.all()
    elif name == "course":
        return list(Course.objects.filter(pageType='c').distinct())
    elif name == "professor":
        return list(Course.objects.filter(pageType='p').distinct())

def getCourseFromQuery(query,pageType):
    courses=[]
    queries=query.split()
    for q in queries:
        courses.extend(list(Course.objects.filter(Q(courseName__icontains=q,pageType=pageType[0])).distinct()))
    
    return list(set(courses))