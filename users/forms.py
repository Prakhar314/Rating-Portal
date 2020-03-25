from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from datetime import datetime
import pytz
from .models import CustomUserModel

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
        elif datetime.now(pytz.utc)>=user.customusermodel.bannedTill:
            pass
        else:
            print(datetime.now(pytz.utc),user.customusermodel.bannedTill)
            raise forms.ValidationError(f"This account is banned till {user.customusermodel.bannedTill}"
        )

class BanForm(forms.Form):
    banDays = forms.IntegerField(label='Number of days to ban(Forever : -1) ',) #widget=forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd hh:mm:ss'}))
    def clean_banDays(self,*args,**kwargs):
        banDays =self.cleaned_data.get("banDays")
        if banDays<-1:
            raise forms.ValidationError("Invalid number of days")
        return banDays