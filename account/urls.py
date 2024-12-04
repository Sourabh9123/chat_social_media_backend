from django.urls import path
from account import views
from account.google_login_new import GoogleLogin
# from accounts.google_login import GoogleLogin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
  
)




urlpatterns = [

    # path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),  # google login
    path('signup/',views.SignUpView.as_view(), name='signup'),
    path('login/',views.LogInview.as_view(), name='login'),
    path('logout/',views.LogOutView.as_view(), name='logout'),
    path('change-passowrd/',views.PasswordChangeView.as_view(), name='password-change'),
    path('google/login/',GoogleLogin.as_view(), name='google-login'),
    path('details/<str:token>/',views.GetUserDetailsByToken.as_view(), name='get-details-by-token' ),
    

    #jwt token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'), # for blacklisting
    
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # for verification
    
]
