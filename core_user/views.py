from rest_framework import viewsets, mixins, status, authentication, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken
from core_user.models import Profile
from core_user.Serializer import UserManagementSerializer, AuthtokenSerializer,GroupSerailizer
from core_user.paginator import StandardResultsSetPagination
from wsgiref.util import FileWrapper
from django.http import HttpResponse
import mimetypes
import os
from rest_framework.settings import api_settings
from django.contrib.auth.models import Group,User
from django.contrib.auth.decorators import permission_required


class TokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthtokenSerializer


class UserManagementView(viewsets.GenericViewSet, mixins.ListModelMixin,
                         mixins.CreateModelMixin, generics.UpdateAPIView, generics.RetrieveAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = UserManagementSerializer
    queryset = Profile.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # @permission_required('auth.view_user')
    def get_queryset(self):
        queryset = Profile.objects.all()
        return queryset

    # @permission_required('auth.view_user')
    def get(self, request, *args, **kwargs):
        return Profile.objects.get(pk=args.get('id'))

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
        if instance is not None:
            instance = instance.auth
            instance.is_active = not instance.is_active
            instance.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], url_path='images', detail=False)
    def download_image(self, request):
        instance = Profile.objects.get(pk=int(request.GET.get('id')))
        path = instance.image
        # print('images/'+path)
        # print(open('images/'+path,'r',errors='ignore').name)
        # print(path)
        wrapper = FileWrapper(path)
        content_type = mimetypes.guess_type(str(path))[0]
        response = HttpResponse(wrapper, content_type=content_type)
        response['Content-Length'] = os.path.getsize(str(path))
        response['Content-Disposition'] = "inline; filename=%s" % path
        return response

    @action(methods=['POST'],url_path='assignRole',detail=False)
    def assign_role(self,request):
        group=request.data['groupId']
        user=request.data['user']
        group = Group.objects.get(pk=group)
        user = User.objects.get(username=user)
        user.groups.set([group])
        return Response(status=status.HTTP_200_OK)


class RoleMangamentView(viewsets.GenericViewSet,mixins.ListModelMixin,
                        generics.RetrieveAPIView,generics.CreateAPIView,generics.UpdateAPIView):
    serializer_class = GroupSerailizer
    queryset = Group.objects.all()

    def get_queryset(self):
        queryset = Group.objects.all()
        return queryset