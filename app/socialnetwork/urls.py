from django.urls import path, include
from rest_framework.routers import DefaultRouter

from socialnetwork import views


router = DefaultRouter()
router.register('posts', views.PostViewSet)
router.register('followers', views.UserFollowerViewSet)
router.register('following', views.UserFollowingViewSet)
router.register('timeline', views.TimelineViewSet)

app_name = 'socialnetwork'

urlpatterns = [
    path('', include(router.urls))
]
