from rest_framework import serializers
from core_user.models import Profile
from django.core.validators import RegexValidator
from django.contrib.auth.models import User



class AuthUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True,write_only=True)
    confirm_email = serializers.CharField(required=True,write_only=True)

    class Meta:
        model = User
        fields = ('id', 'password', 'last_login', 'is_superuser', 'username',
                  'first_name', 'last_name', 'email', 'is_staff',
                  'is_active', 'date_joined', 'confirm_password','confirm_email')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        read_only_fields = ('id', 'last_login')

    def validate(self, data):
        confirm_pass = data.get('confirm_password',None)
        password = data.get('password',None)
        if confirm_pass != password:
            raise serializers.ValidationError("Password and confirm password are not same")
        confirm_email = data.get('confirm_email',None)
        email = data.get('email',None)
        if confirm_email != email:
            raise serializers.ValidationError("email and confirm email are not same")
        return data





class UserManagementSerializer(serializers.ModelSerializer):
    auth = AuthUserSerializer()
    gender = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    contact = serializers.IntegerField(required=False,validators=[RegexValidator(regex='^[0-9]{10}$',message='Please enter valid contact number')])
    class Meta:
        model = Profile
        fields = ('user_id','auth','gender','city','country','contact','image')

    def create(self, validated_data):
        user_data = validated_data.pop('auth')
        user_data.pop('confirm_password')
        user_data.pop('confirm_email')
        user = User.objects.create(**user_data)
        profile = Profile.objects.create(auth=user, **validated_data)
        return profile
