from rest_framework import serializers, exceptions
from rest_framework.permissions import BasePermission
from core_user.models import Profile
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate
from django.contrib.auth.models import User,Group,Permission
from django.db.models import ObjectDoesNotExist

class PermissionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    codename = serializers.CharField()

    class Meta:
        model = Permission
        fields = ('id','name','codename')


class GroupSerailizer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    permissions = serializers.ListSerializer(child=PermissionSerializer(),required=True)

    def create(self, validated_data):
        permissions = validated_data.pop('permissions')
        group = Group.objects.create(**validated_data)
        for permission in permissions:
            permissionFromDb = Permission.objects.get(pk=permission.get('id'))
            group.permissions.add(permissionFromDb)
        return group



    class Meta:
        model = Group
        fields = ('id','name','permissions')





class AuthUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=False, write_only=True)
    confirm_email = serializers.CharField(required=False, write_only=True)
    password = serializers.CharField(required=False,write_only=True,min_length=5)
    username = serializers.CharField(required=True)
    groups = serializers.ListSerializer(child=GroupSerailizer(),read_only=True)

    class Meta:
        model = User
        fields = ('id', 'password', 'last_login', 'is_superuser', 'username',
                  'first_name', 'last_name', 'email', 'is_staff',
                  'is_active', 'date_joined', 'confirm_password', 'confirm_email','groups')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        read_only_fields = ('id', 'last_login')

    def validate(self, data):
        if self.context['request']._request.method == 'POST':
            confirm_pass = data.get('confirm_password', None)
            password = data.get('password', None)
            username = data.get('username', None)

            try:
             User.objects.get(username=username)
             raise serializers.ValidationError("User with username already exists")
            except ObjectDoesNotExist:
             print("ok")

            if password is None:
                raise serializers.ValidationError("Password is required")
            if confirm_pass != password:
                raise serializers.ValidationError("Password and confirm password are not same")
            confirm_email = data.get('confirm_email', None)
            email = data.get('email', None)
            if confirm_email != email:
                raise serializers.ValidationError("email and confirm email are not same")
            return data
        else:
            return data


class AuthtokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(request=self.context.get('request'), username=username, password=password)
        if not user:
            msg = ('Not a valid credentials')
            raise exceptions.AuthenticationFailed(msg)

        attrs['user'] = user
        return attrs


class UserManagementSerializer(serializers.ModelSerializer):
    auth = AuthUserSerializer()
    gender = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    contact = serializers.IntegerField(required=False, validators=[
        RegexValidator(regex='^[0-9]{10}$', message='Please enter valid contact number')])

    class Meta:
        model = Profile
        fields = ('user_id', 'auth', 'gender', 'city', 'country', 'contact', 'image')

    def create(self, validated_data):
        user_data = validated_data.pop('auth')
        user_data.pop('confirm_password')
        user_data.pop('confirm_email')
        user = User.objects.create(**user_data)
        user.set_password(user.password)
        user.save()
        profile = Profile.objects.create(auth=user, **validated_data)
        return profile

    def update(self, profile, validated_data):
        user_data = validated_data.pop('auth')
        user_data['password'] = profile.auth.password
        user_data['username'] = profile.auth.username
        user_data.id = profile.auth.id
        User.objects.update_or_create(defaults=user_data,id=user_data.id)
        for k, v in validated_data.items():
            setattr(profile, k, v() if callable(v) else v)
        user = User.objects.get(pk=user_data.id)
        profile.auth = user
        profile.save()
        return profile
