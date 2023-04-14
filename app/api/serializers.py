from rest_framework import serializers
from api.models import *
from django.utils.encoding import smart_str , force_bytes ,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode ,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError

class MyUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = MyUser
        fields = ['email', 'name','tc', 'password', 'password2']
        extra_kwargs = {
            'password':{'write_only':True},
        }
    
    def validate(self, data):
        pass1 = data.get('password')
        pass2 = data.get('password2')
        if pass1 != pass2:
            raise serializers.ValidationError('password and confirm password dont matching')
        return data
    
    def create(self, validate_data):
        return MyUser.objects.create_user(**validate_data)
    

class UserLoginSerialiser(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255) # this field has to be override otherwise while requesting post it will try to create an instance while authenticating
    class Meta:
        model = MyUser
        fields = ['email','password']

class UserProfileSerialiser(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id','email', 'name',]
    


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['name']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class UserChangePasswordSerialiser(serializers.Serializer):
    password = serializers.CharField(max_length=255 , style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255 , style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password','password2']
    
    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.get('password2')
        user = self.context.get('user')
        if pass1 != pass2:
            raise serializers.ValidationError('password and confirm password dont matching')
        # attrs['password']=pass1   # pass extraa dict to valdated data
        user.set_password(pass1)
        user.save()
        return attrs
    
class SendPasswordResetEmailSerialiser(serializers.Serializer):
    email = serializers.EmailField(max_length=255) 
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        user_exist = MyUser.objects.filter(email=email).exists()
        if user_exist:
            user = MyUser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:api/user/reset-password/' + uid +'/' + token
            print(link)
            return attrs
        else:
            raise serializers.ValidationError('no user exists  , please give correct email') 
        


class UserResetChangePasswordEmailSerialiser(serializers.Serializer):
    password = serializers.CharField(max_length=255 , style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255 , style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password','password2']
    
    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.get('password2')
        user_id = self.context.get('uid')
        token = self.context.get('token')
        if pass1 != pass2:
            raise serializers.ValidationError('password and confirm password dont matching')
        id = smart_str(urlsafe_base64_decode(user_id))
        user = MyUser.objects.get(id=id)
        if PasswordResetTokenGenerator().check_token(user,token):
            user.set_password(pass1)
            user.save()
        else:
            raise ValidationError('token is not valid')
        return attrs
    
  

    