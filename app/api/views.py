from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api.serializers import *
from django.contrib.auth import authenticate
from api.renderers import *
from api.token import *
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class UserRegistrationView(APIView):
    renderer_classes = [MyUserRenderers]
    def post(self, request , format=None):
        serializer = MyUserSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save() 
            print(user)
            token = get_tokens_for_user(user)
            return Response({'msg':'registration done', 'toke': token})
        return Response(serializer.errors , status= status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes = [MyUserRenderers]
    def post(self, request , format=None):
        serializer = UserLoginSerialiser(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'msg':'login success', 'toke': token})
            else:
                return Response({'error':{'non_field_errors':['email or password is not valid']}}, status= status.HTTP_400_BAD_REQUEST)            


class UserProfileView(APIView):
    renderer_classes = [MyUserRenderers]
    permission_classes = [IsAuthenticated]
    def get(self, request , format=None):
        serializer = UserProfileSerialiser(request.user)
        return Response(serializer.data)

class UserProfileUpdate(APIView):
    renderer_classes = [MyUserRenderers]
    permission_classes = [IsAuthenticated] 
    def patch(self, request, format=None):
        user = request.user
        user_obj = MyUser.objects.get(id=user.id)
        serializer = UserProfileUpdateSerializer(user_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'updated'})
        

class UserChangePaswwordView(APIView):
    renderer_classes = [MyUserRenderers]
    permission_classes = [IsAuthenticated]
    def post(self, request , format=None):
        serializer = UserChangePasswordSerialiser(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            # user = request.user
            # password = serializer.validated_data.get('password')      # this is another way to handel other than doing this in serializer validate 
            # user.set_password(password)
            # user.save()
            return Response({'msg':'succesfully password changed'})
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmailView(APIView):
    renderer_classes = [MyUserRenderers]
    def post(self, request , format=None):
        serializer = SendPasswordResetEmailSerialiser(data=request.data )
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'password change link is send to the email'})
        
class ResetPasswordResetEmailView(APIView):
    renderer_classes = [MyUserRenderers]
    def post(self, request , uid , token, format=None):
        serializer = UserResetChangePasswordEmailSerialiser(data=request.data, context={'uid': uid , 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'succesfully password changed'})
  
        

           