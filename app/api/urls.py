from django.urls import path
from api.views import *
urlpatterns = [

    path('register/', UserRegistrationView.as_view() , name='register'),
    path('login/', UserLoginView.as_view() , name='login'),
    path('userprofile/', UserProfileView.as_view() , name='userprofile'),
    path('userprofile-update/', UserProfileUpdate.as_view() , name='userprofile_update'),
    path('changepassword/', UserChangePaswwordView.as_view() , name='changepassword'),
    path('change-password-email/', SendPasswordResetEmailView.as_view() , name='change-password-email'),
    path('reset-password/<uid>/<token>/', ResetPasswordResetEmailView.as_view() , name='reset-password'),
]
