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
        fields = ["first_name","last_name","username", "email", "password1", "password2"]

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        emailPre = email.split('@')[0]
        for alreadyPre in [u.email.split('@')[0] for u in User.objects.all()]:
            if (emailPre.startswith(alreadyPre) or alreadyPre.startswith(emailPre)) and alreadyPre!='' and emailPre!='' :
                print(emailPre,alreadyPre)
                raise forms.ValidationError("Email already in use")
        if emailPre=='':
            raise forms.ValidationError("Use a valid IIT-D email")
        if not email.endswith("iitd.ac.in"):
            raise forms.ValidationError("Use a valid IIT-D email")
        return email

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        if username == 'Anonymous':
            raise forms.ValidationError("Username not allowed")
        return username


class PickyAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.customusermodel.bannedTill:
            pass
        elif datetime.now(pytz.utc) >= user.customusermodel.bannedTill:
            pass
        else:
            print(datetime.now(pytz.utc), user.customusermodel.bannedTill)
            raise forms.ValidationError(
                f"This account is banned till {user.customusermodel.bannedTill}"
            )


class BanForm(forms.Form):
    banDays = forms.IntegerField(
        label="Number of days to ban(Forever : -1) ",
    )  # widget=forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd hh:mm:ss'}))

    def clean_banDays(self, *args, **kwargs):
        banDays = self.cleaned_data.get("banDays")
        if banDays < -1:
            raise forms.ValidationError("Invalid number of days")
        return banDays
