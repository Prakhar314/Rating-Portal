"""ratingPortal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

import users.views as user_views
import courses.views as courseViews
import review.views as reviewViews
from users.forms import PickyAuthenticationForm


urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", user_views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="users/login.html",
            authentication_form=PickyAuthenticationForm,
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path("", user_views.homeView, name="home"),
    path("profile/<str:profileOwner>/", user_views.profile, name="profile"),
    path("change-pass/", user_views.changePassword, name="change-pass"),
    path("course/<int:courseID>/", courseViews.courseView, name="course"),
    path("professor/<int:courseID>/", courseViews.courseView, name="professor"),
    path("course/", courseViews.courseListView, name="courseList",kwargs={'pageType':'course'}),
    path("professor/", courseViews.courseListView, name="professorList",kwargs={'pageType':'professor'}),
    path("issues/", reviewViews.issueView, name="issues"),
    path("delete/<int:reviewID>/", reviewViews.deleteReview, name="delete"),
    path("report/<int:reviewID>/", reviewViews.reportFormView, name="report"),
    path("ignore/<int:reviewID>/", reviewViews.ignoreReports, name="ignore"),
    path(
        "reportAction/<int:reviewID>/",
        reviewViews.adminReportAction,
        name="reportAction",
    ),
    path("ban/<int:userID>/<int:reviewID>/", user_views.banView, name="ban"),
    path("new/",courseViews.courseFormView,name ="new"),
    path("all/",reviewViews.viewAllReviews,name ="all"),
    path("top/",user_views.topProfilesView,name ="top"),
]
