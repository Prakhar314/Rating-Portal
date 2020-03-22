from django.db import models

class Course(models.Model):
    courseName = models.CharField(max_length=120)
    rating = models.DecimalField(decimal_places=2,max_digits=4)
    noOfReviews = models.IntegerField()
    class Meta:
        ordering = ['courseName']
