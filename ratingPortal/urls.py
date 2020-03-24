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
import users.views as user_views
import courses.views as courseViews
import review.views as reviewViews

from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',user_views.register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('',user_views.homeView,name='home'),
    path('profile/<str:profileOwner>/',user_views.profile,name='profile'),
    path('change-pass/',user_views.changePassword,name='change-pass'),
    path('course/<str:courseName>/',courseViews.courseView,name='course'),
    path('course/',courseViews.courseListView,name='courseList'),
    path('issues/',reviewViews.issueView,name='issues'),
    path('delete/<int:reviewID>/<str:type>/',reviewViews.deleteReview,name='delete'),
    path('report/<int:reviewID>/',reviewViews.reportFormView,name='report'),
]
