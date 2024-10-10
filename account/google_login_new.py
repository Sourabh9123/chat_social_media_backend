from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from oauth2_provider.models import Application
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
import requests
import json
import jwt
from account.views import get_tokens_for_user
User = get_user_model()



import pprint
from django.contrib.auth.hashers import make_password


class GoogleLogin(APIView):
    def post(self, request):
        data = request.data['decode_data']
      
        
        first_name = data.get('given_name')
        last_name = data.get('family_name')
        email = data.get('email')
        password = "normalpassword@9123"
        hashed_password = make_password(password)



        user , created = User.objects.get_or_create(
            email=email, first_name=first_name, last_name=last_name
        )
        

        if  created:
            user.password = hashed_password
            user.save()
            auth_user = authenticate(request, username=email,password=password, )
            if auth_user is not None:
                current_user = User.objects.get(email=email)
                token = get_tokens_for_user(user=current_user)
                login(request, auth_user)
                # print(token)
                return Response({"token":token}, status=status.HTTP_200_OK)

       
        auth_user = authenticate(request, username=email, password=password, )
        if auth_user is not None:
            current_user = User.objects.get(email=email)
            token = get_tokens_for_user(user=current_user)
            login(request, auth_user)
            # print(token,"---------------------------------------")
            return Response({"token":token}, status=status.HTTP_200_OK)
       
       
        # access_token = request.data.get('access_token')
        # print(access_token)
        
        
        return Response({'error': 'Google token verification sucess'}, status=status.HTTP_200_OK)

        return Response({'error': 'Google token verification failed'}, status=status.HTTP_401_UNAUTHORIZED)


















































# class GoogleLogin(APIView):
#     def post(self, request):
#         print('-----------------------------------------------')
#         # Get the Google access token from the frontend
#         print(request.data["data_user"])

        
       
#         # access_token = request.data.get('access_token')
#         # print(access_token)
#         user_credintial = request.data['data_user']['credential']
#         # print(user_credintial)

#         # Verify the Google access token
#         google_response = requests.get(
#             'https://www.googleapis.com/oauth2/v3/userinfo',
#             params={'user_credintial': user_credintial}
#         )
#         google_data = google_response.json()

#         print(google_data)

#         if google_response.status_code == 200:
#             # Check if a user with the Google ID exists
#             user, created = User.objects.get_or_create(username=google_data['sub'])

#             # Create or update user's information as needed
#             user.email = google_data.get('email', '')
#             user.first_name = google_data.get('given_name', '')
#             user.last_name = google_data.get('family_name', '')
#             user.save()

#             # Create an OAuth2 application (if not already created)
#             application, created = Application.objects.get_or_create(
#                 name='Google App',
#                 client_id='46446715863-rlfm27iovjurakn4kagcnrmscc2me86n.apps.googleusercontent.com',
#                 client_secret='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',
#                 user=user
#             )

#             # Issue an OAuth2 access token
#             response_data = {
#                 'access_token': application.user_token.access_token,
#                 'token_type': 'Bearer',
#             }

#             return Response(response_data, status=status.HTTP_200_OK)

#         return Response({'error': 'Google token verification failed'}, status=status.HTTP_401_UNAUTHORIZED)
