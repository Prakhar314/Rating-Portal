from .models import Course
from django import forms


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ("courseName","courseDescription","pageType")

    def clean_courseName(self, *args, **kwargs):
        courseName = self.cleaned_data.get("courseName")
        if courseName in [c.courseName for c in Course.objects.all()]:
            raise forms.ValidationError("Page already exists")
        return courseName
