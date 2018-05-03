from django.conf.urls import include
from django.conf.urls import url
from django.contrib.auth.views import logout
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.views import password_change
from django.contrib.auth.views import password_change_done
from django.contrib.auth.views import password_reset
from django.contrib.auth.views import password_reset_complete
from django.contrib.auth.views import password_reset_confirm
from django.contrib.auth.views import password_reset_done
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

from . import views
from .views import *

router = routers.SimpleRouter()
router.register(r'max-lifts', MaxLiftTrackingViewSet, base_name='max-lift-tracking')
router.register(r'body-stats', BodyStatTrackingViewSet, base_name='body-stat-tracking')
router.register(r'users', UserViewSet, base_name='users')
router.register(r'workouts', WorkoutViewSet, base_name='user-workouts')
router.register(r'exercise', ExerciseViewSet, base_name='user-exercise')
router.register(r'exercises', ExercisesViewSet, base_name='exercises-list')
router.register(r'friends', FriendsViewSet, base_name='friends')
router.register(r'friend-workouts', FriendWorkoutViewSet, base_name='friend-workouts')
router.register(r'workout-copy', CopyFriendWorkoutViewSet, base_name='workout-copy')
router.register(r'account-settings', AccountSettingsViewSet, base_name='account-settings')
router.register(r'friend-profile', FriendProfileUserViewSet, base_name='friend-profile')

urlpatterns = [

    url(r'^logout/$', logout, {'template_name': 'accounts/signout.html'}, name='logout'),
    url(r'^logout-then-login/$', logout_then_login, name='logout_then_login'),
    url(r'^password-change/$', password_change, name='password_change'),
    url(r'^password-change/done/$', password_change_done, name='password_change_done'),
    url(r'^password-reset/$', password_reset, name='password_reset'),
    url(r'^password-reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', password_reset_complete, name='password_reset_complete'),



    url(r'^v1/', include(router.urls)),
    url(r'^v1/users/find', views.UserSearchListView.as_view()),
    url(r'^v1/friends/find', views.FriendSearchListView.as_view()),
    url(r'^v1/workout/send/$', views.SendWorkoutEmail.as_view()),
    url(r'^v1/user/create/$', views.CreateUser.as_view()),
    url(r'^v1/exercises-list/$', views.ExercisesList.as_view()),
    url(r'^v1/u/workouts/$', views.WorkoutList.as_view()),
    url(r'^v1/history/$', views.ProfileHistory.as_view()),
    url(r'^v1/follow/$', views.FollowView.as_view()),
    url(r'^v1/user/friends/$', views.FriendsView.as_view()),
    url(r'^v1/forgot-password-reset/$', views.ForgotPasswordReset.as_view()),
    url(r'^v1/reset-password-confirm/$', views.ConfirmPasswordReset.as_view()),


    url(r'^v1/login/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),


    # url(r'^$', views.index, name='index'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
