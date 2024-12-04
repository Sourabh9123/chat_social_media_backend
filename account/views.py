from django.shortcuts import render
from rest_framework.views import  APIView  
# from django.contrib.auth.models import User
from account.models import User
from rest_framework.response import Response
from rest_framework import status
from account.serializers import LoginSerializer, PasswordChangeSerializer,  UserSerializer
from django.contrib.auth import authenticate, login, logout 
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password




from django.contrib.auth import get_user_model
User = get_user_model()


# #costume token
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Add custom claims
#         token['email'] = user.email

#         return token




def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



#    "password": "9123",
#     "email": "admin1@gmai.com",
#     "first_name": "test",
#   "last_name": "tws"
  


from django.conf import settings
# SECRET_KEY
from account.decoted_jwt import decode_jwt_token

class GetUserDetailsByToken(APIView):

    def get(self, request, *args, **kwargs):
        access_token = kwargs.get("token")
        # print(access_token, "-------")
        # print("sec ------ key ", settings.SECRET_KEY)

        user_id = decode_jwt_token(token=access_token , token_secret=settings.SECRET_KEY)
        print(user_id, " -------------------")
        if  user_id is None:
            print("inside the condition-------------")
            return Response({"data" :"invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        
        instance = User.objects.get(id=user_id)
        serializer = UserSerializer(instance)
        data = serializer.data
        data["token"] = get_tokens_for_user(instance)
 
        return Response({"data" :data}, status=status.HTTP_200_OK)



        # return Response({"data": })



class SignUpView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        print(request.data, "------------------------------------------")
        if request.data.get('email'):
            request.data['email'] = request.data.get('email').lower()
        serializer = UserSerializer(data=request.data)
     

        if "email" in request.data:
            user = User.objects.filter(email=request.data.get("email"))
            if user:
                print("user already exists -    -    -  ")
                return Response("please change your email or login this email is alredy register",status=status.HTTP_400_BAD_REQUEST)
       
        
       
        if serializer.is_valid():
            password = make_password(serializer.validated_data['password'])
            serializer.validated_data['password'] = password

            serializer.save()
            user = User.objects.get(email=serializer.validated_data['email'])
            token = get_tokens_for_user(user)
            # user = request.user()LO
        
            # print({'token':token, 'data' :serializer.data})
            
            return Response({'token':token, 'data' :serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogInview(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        if request.data.get('email'):
            request.data['email'] = request.data.get('email').lower()
  
        serializer  = LoginSerializer(data=request.data)

        is_user = User.objects.filter(email=request.data['email']).exists()
    
      

        try:
            if serializer .is_valid():
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']
                user= authenticate(request, username=email, password=password)
                login(request, user)
                # user_authenticate = authenticate(request, username=email, password=password)
                # print("----------------authenticated", user_authenticate)
                

                user_personal_data = User.objects.get(email=email)
                user_data = UserSerializer(user_personal_data)
                

                token = get_tokens_for_user(user)
        
                response_data = serializer.data 
                response_data['token'] =  token
                response_data['user_data'] =  user_data.data
                
                return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:

            if is_user:
                return Response({'message':'password does not match'},status=status.HTTP_400_BAD_REQUEST )
            return Response({'message':'user does not exist'},status=status.HTTP_400_BAD_REQUEST )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
         








    

"""{

"email" : "sourabhd081@gmail.com",
"password": "9123"

}"""




       

class LogOutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        # print(request.data)
        # access = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        access_token = request.auth
        refresh_token =  request.data.get('refresh_token')
    
        refresh = RefreshToken(refresh_token)
        refresh.blacklist()

        
        # logout(user)
        logout(request)
        return Response({"message":"user logged out successfully"}, status=status.HTTP_200_OK)
        
            
# refresh = RefreshToken()
        # access_token.blacklist()
        # access_token.blacklist()
        # refresh.blacklist()

   

class PasswordChangeView(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self, request,  format=None):
        token = request.META.get('HTTP_AUTHORIZATION', '')
    

        #need to decode access toke and then request user and made change password
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            
            print(user)
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        