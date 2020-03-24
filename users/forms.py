from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone as datetime

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields=['username','email','password1','password2']

    def clean_email(self,*args,**kwargs):
        email =self.cleaned_data.get("email")
        if not email.endswith("iitd.ac.in"):
            raise forms.ValidationError("Use a valid IIT-D email")
        return email

class PickyAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.customusermodel.bannedTill:
            pass
        elif datetime.now()>=user.customusermodel.bannedTill:
            pass
        else:
            raise forms.ValidationError(f"This account is banned till {user.customusermodel.bannedTill}"
        )
