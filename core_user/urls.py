from django.urls import path,include
from rest_framework.routers import DefaultRouter

from core_user import  views

router = DefaultRouter()
router.register('', viewset=views.UserManagementView)
app_name = 'core_user'

urlpatterns = [
    path('',include(router.urls)),
    # path('images/<str:path>/',views.UserManagementView.download_image)
]