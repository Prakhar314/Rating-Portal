from django.db import models
from django.contrib.auth.models import User
class Review(models.Model):
    score = models.DecimalField(decimal_places=2,max_digits=4)
    reviewContent = models.TextField()
    courseName = models.CharField(max_length=120)
    dateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='reviews_written',default=5)
    class Meta:
        ordering =['-dateAdded']

class Report(models.Model):
    reviewReported = models.ForeignKey(Review, on_delete= models.CASCADE,related_name='flags',blank=True,null=True)
    reportReason = models.TextField()
    dateReported = models.DateTimeField(auto_now=False, auto_now_add=True)
    class Meta:
        ordering =['dateReported']