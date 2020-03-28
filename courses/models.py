from django.db import models

class Course(models.Model):

    TYPE_OF_PAGE=[('c','Course'),('p','Professor')]

    courseName = models.CharField(max_length=120)
    rating = models.DecimalField(decimal_places=2,max_digits=4,default=-1)
    noOfReviews = models.IntegerField(default=0)
    courseDescription = models.TextField(default='')
    pageType = models.CharField(
        max_length=1,
        choices=TYPE_OF_PAGE,
        default='c',
        )

    class Meta:
        ordering = ['courseName']
