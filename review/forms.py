from .models import Review
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('score','reviewContent')