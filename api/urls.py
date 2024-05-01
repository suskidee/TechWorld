from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register('post', views.ApiPost, basename='Blog_post')
router.register('category', views.ApiCategory, basename='category')

post_router = routers.NestedDefaultRouter(router, 'post', lookup='post')
post_router.register('comment', views.ApiComment, basename='post_comment')

urlpatterns = [
    path("", include(router.urls)),
    path("", include(post_router.urls)),

]

