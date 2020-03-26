from .models import Review, Report
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("score", "reviewContent","isAnonymous")

    def clean_score(self, *args, **kwargs):
        score = self.cleaned_data.get("score")
        if not 0 <= score <= 10:
            raise forms.ValidationError("Score must be between 0 and 10")
        return score


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ("reportReason",)

