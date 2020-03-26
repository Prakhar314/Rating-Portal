from django.db import models
from django.contrib.auth.models import User
class Review(models.Model):
    score = models.DecimalField(decimal_places=2,max_digits=4)
    reviewContent = models.TextField()
    courseName = models.CharField(max_length=120)
    dateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='reviews_written')
    class Meta:
        ordering =['-dateAdded']

    def flaggers(self):
        return [u.reporter for u in self.flags.all()]
    def getTotalLikes(self):
        return self.likes.users.count()
    def getTotalDislikes(self):
        return self.dislikes.users.count()

class Report(models.Model):
    reviewReported = models.ForeignKey(Review, on_delete= models.CASCADE,related_name='flags',blank=True,null=True)
    reportReason = models.TextField()
    dateReported = models.DateTimeField(auto_now=False, auto_now_add=True)
    reporter = models.TextField(default='')
    class Meta:
        ordering =['dateReported']

class RecentAction(models.Model):
    TYPE_OF_ACTION=[('a','Alert'),('i','info')]

    user = models.ForeignKey(User, on_delete= models.CASCADE,related_name='recentActions')
    dateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)
    actionDetail = models.TextField()
    actionLink = models.TextField(blank=True,null=True)
    actionType = models.CharField(
        max_length=1,
        choices=TYPE_OF_ACTION,
        default='i',
    )
    class Meta:
        ordering =['-dateAdded']

    @classmethod
    def create(cls, user,actionDetail,actionType,actionLink=None):
        action = cls(user=user,actionDetail=actionDetail,actionLink=actionLink,actionType=actionType)
        return action

class Like(models.Model):

    review = models.OneToOneField(Review, related_name="likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='reviewLikes')
    dateAdded = models.DateTimeField(auto_now_add=True)

class DisLike(models.Model):

    review = models.OneToOneField(Review, related_name="dislikes", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='reviewDislikes')
    dateAdded = models.DateTimeField(auto_now_add=True)
