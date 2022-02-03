from django.urls import path,include
from rest_framework.routers import DefaultRouter

from core_user import  views

router = DefaultRouter()
router.register('user', viewset=views.UserManagementView)
router.register('role',viewset=views.RoleMangamentView)

app_name = 'core_user'

urlpatterns = [
    path('',include(router.urls)),
    path('token', views.TokenView.as_view(),name='token')
    # path('images/<str:path>/',views.UserManagementView.download_image)
]