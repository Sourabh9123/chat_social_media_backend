# from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from post_app.models import Post
# from account.models import User
from django.contrib.auth import get_user_model
from post_app.models import Like
import json
User = get_user_model()



class PostTest(APITestCase):

    def setUp(self):
        self.url = reverse("post_list")
        self.user = User.objects.create(
            email="abc912@gmail.com",
            first_name = "abcd",
            last_name = "das",
            username = "ausername"
        )


    def test_create_post_authenticated(self):
        self.client.force_authenticate(self.user)
        data = {
            "title" : "test from"
        }
        response = self.client.post(
            self.url, data=data, format="json"
        )
        
  
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        
        self.assertEqual(response.data['data']["title"], data["title"])
        self.assertEqual(response.data['data']["author"]['id'], str(self.user.id))


    def test_list_post(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(
            self.url
        )
        self.assertEqual(
            response.status_code,status.HTTP_200_OK
        )
    
    def test_list_details(self):
        self.client.force_authenticate(self.user)
        data = {
            "title" : "test from "
        }
        post = self.client.post(
            self.url, data=data, format="json"
        )

        res = self.client.get(
            self.url, kwargs={"post_id": post.data['data']['author']['id']}
        )
        self.assertEqual(
            res.status_code , status.HTTP_200_OK
        )




class LikeModelTest(APITestCase):

    def setUp(self):
        
        self.user = User.objects.create(
            email="abc912@gmail.com",
            first_name = "abcd",
            last_name = "das",
            username = "ausername"
        )

        self.post = Post.objects.create(
            author_id= self.user.id,
            title = "a test"
        )
        self.url = reverse('create_or_list_like', kwargs={"post_id":self.post.id})

    
    def test_like_post(self):
        
        self.client.force_authenticate(self.user)
     
        user_id = self.user.id
        
        response = self.client.post(
            self.url, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_likes(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(
            self.url,

        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)