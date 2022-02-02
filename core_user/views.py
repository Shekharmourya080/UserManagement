from rest_framework import viewsets, mixins, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from core_user.models import Profile
from core_user.Serializer import UserManagementSerializer
from core_user.paginator import StandardResultsSetPagination
from wsgiref.util import FileWrapper
from django.http import HttpResponse
import mimetypes
import os

class UserManagementView(viewsets.GenericViewSet, mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    pagination_class = StandardResultsSetPagination
    serializer_class = UserManagementSerializer
    queryset = Profile.objects.all()

    def get_queryset(self):
        queryset = Profile.objects.all()
        return queryset

    @action(methods=['delete'], url_path='delete', detail=False)
    def delete(self, request):
        id = int(request.GET.get('id'))
        instance = Profile.objects.filter(pk=id)
        instance.delete()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['put'], url_path='changeStatus', detail=False)
    def toggleStatus(self, request):
        id = int(request.GET.get('id'))
        instance = Profile.objects.get(pk=id)
        if instance != None:
            instance = instance.auth
            instance.is_active = not instance.is_active
            instance.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], url_path='images', detail=False)
    def download_image(self,request):
        instance = Profile.objects.get(pk=int(request.GET.get('id')))
        path = instance.image
        wrapper = FileWrapper(path)
        content_type = mimetypes.guess_type(str(path))[0]
        response = HttpResponse(wrapper, content_type=content_type)
        response['Content-Length'] = os.path.getsize(str(path))
        response['Content-Disposition'] = "attachment; filename=%s" % path
        return response
