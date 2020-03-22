from django.db import models

class Review(models.Model):
    name = models.CharField(max_length=120)
    score = models.DecimalField(decimal_places=2,max_digits=4)
    reviewContent = models.TextField()
    courseName = models.CharField(max_length=120)