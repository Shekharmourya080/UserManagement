from rest_framework import serializers
from core_user.models import Profile
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class AuthUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ('id','password','last_login','is_superuser','username',
                  'first_name','last_name','email','is_staff',
                  'is_active','date_joined')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        read_only_fields = ('id','last_login')


class UserManagementSerializer(serializers.ModelSerializer):
    auth = AuthUserSerializer()

    gender = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    contact = serializers.IntegerField(required=True,validators=[RegexValidator(regex='^[0-9]{10}$',message='Please enter valid contact number')])
    class Meta:
        model = Profile
        fields = ('user_id','auth','gender','city','country','contact')

    def create(self, validated_data):
        user_data = validated_data.pop('auth')
        user = User.objects.create(**user_data)
        profile = Profile.objects.create(auth=user, **validated_data)
        return profile