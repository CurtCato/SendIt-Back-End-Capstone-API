from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from SendItApp.models import *
from SendItApp.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'classesoffered', ClassesOffered, 'classoffered')
router.register(r'climbers', Climbers, 'climber')
router.register(r'climbingtypes', ClimbingTypes, 'climbingtype')
router.register(r'gyms', Gyms, 'gym')
router.register(r'users', Users, 'user')
router.register(r'gymtypes', GymTypes, 'gymtype')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register$', register_user),
    url(r'^login$', login_user),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^api-auth$', include('rest_framework.urls', namespace='rest_framework')),
]