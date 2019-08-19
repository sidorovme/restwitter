from rest_framework.test import APIClient, APITestCase
import json
from rest_framework import status
from django.contrib.auth.models import User, Permission

client = APIClient()

class RemoteAuthenticatedTest(APITestCase):
    
    def setUp(self):
        self.permission_addtweet = Permission.objects.get(name='Can add tweet')
        self.permission_changetweet = Permission.objects.get(name='Can change tweet')
        self.permission_deletetweet = Permission.objects.get(name='Can delete tweet')
        self.permission_viewtweet = Permission.objects.get(name='Can view tweet')

        self.user1_name = 'user1'
        self.user1_pass = 'F@kePass1'
        self.user1 = User.objects.create_user(username=self.user1_name, password=self.user1_pass)
        self.user1.user_permissions.add(self.permission_addtweet)
        self.user1.user_permissions.add(self.permission_changetweet)
        self.user1.user_permissions.add(self.permission_deletetweet)
        self.user1.user_permissions.add(self.permission_viewtweet)

        self.user2_name = 'user2'
        self.user2_pass = 'F@kePass2'
        self.user2 = User.objects.create_user(username=self.user2_name, password=self.user2_pass)
        self.user2.user_permissions.add(self.permission_addtweet)
        self.user2.user_permissions.add(self.permission_changetweet)
        self.user2.user_permissions.add(self.permission_deletetweet)
        self.user2.user_permissions.add(self.permission_viewtweet)

        self.apiurl = '/api/tweets/'
        self.valid_tweet = json.dumps({"text": "valid tweet"})
        self.content_type = 'application/json'
    

    def test_tweet_list_unauthenticated(self):
        response = self.client.get(self.apiurl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # Add tweet without authentication forbidden
    def test_tweet_create_unauthenticated(self):
        response = client.post(
            self.apiurl,
            data=self.valid_tweet,
            content_type=self.content_type
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    # Add tweet with authentication
    def test_tweet_create_authenticated(self):
        self.assertTrue(client.login(username=self.user1_name, password=self.user1_pass))
        response = client.post(
            self.apiurl,
            data=self.valid_tweet,
            content_type=self.content_type
        )
        tweet_id = response.data['id']
        client.logout()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    # Modify own tweet
    def test_tweet_modify_own(self):
        
        # create tweet
        self.assertTrue(client.login(username=self.user1_name, password=self.user1_pass))
        response = client.post(
            self.apiurl,
            data=self.valid_tweet,
            content_type=self.content_type
        )
        tweet_id = response.data['id']
        client.logout()

        # modify tweet
        client.login(username=self.user1_name, password=self.user1_pass)
        response = client.put(
            "%s%d/" % (self.apiurl, tweet_id),
            data=json.dumps({"text": "something else"}),
            content_type=self.content_type
        )
        client.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # Modify other's tweet
    def test_tweet_modify_others(self):
        
        # create tweet
        self.assertTrue(client.login(username=self.user1_name, password=self.user1_pass))
        response = client.post(
            self.apiurl,
            data=self.valid_tweet,
            content_type=self.content_type
        )
        tweet_id = response.data['id']
        client.logout()

        # modify tweet
        client.login(username=self.user2_name, password=self.user2_pass)
        response = client.put(
            "%s%d/" % (self.apiurl, tweet_id),
            data=json.dumps({"text": "something else"}),
            content_type=self.content_type
        )
        client.logout()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    # Modify unauthenticated
    def test_tweet_modify_unauthenticated(self):
        
        # create tweet
        self.assertTrue(client.login(username=self.user1_name, password=self.user1_pass))
        response = client.post(
            self.apiurl,
            data=self.valid_tweet,
            content_type=self.content_type
        )
        tweet_id = response.data['id']
        client.logout()

        # modify tweet
        response = client.put(
            "%s%d/" % (self.apiurl, tweet_id),
            data=json.dumps({"text": "something else"}),
            content_type=self.content_type
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    # Delete own tweet
    def test_tweet_delete_own(self):
        
        # create tweet
        self.assertTrue(client.login(username=self.user1_name, password=self.user1_pass))
        response = client.post(
            self.apiurl,
            data=self.valid_tweet,
            content_type=self.content_type
        )
        tweet_id = response.data['id']
        client.logout()

        # delete tweet
        client.login(username=self.user1_name, password=self.user1_pass)
        response = client.delete(
            "%s%d/" % (self.apiurl, tweet_id),
            data=json.dumps({"text": "something else"}),
            content_type=self.content_type
        )
        client.logout()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    
    # Delete other's tweet
    def test_tweet_delete_own(self):
        
        # create tweet
        self.assertTrue(client.login(username=self.user1_name, password=self.user1_pass))
        response = client.post(
            self.apiurl,
            data=self.valid_tweet,
            content_type=self.content_type
        )
        tweet_id = response.data['id']
        client.logout()

        # delete tweet
        client.login(username=self.user2_name, password=self.user2_pass)
        response = client.delete(
            "%s%d/" % (self.apiurl, tweet_id),
            data=json.dumps({"text": "something else"}),
            content_type=self.content_type
        )
        client.logout()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    # Delete unauthenticated
    def test_tweet_delete_unauthenticated(self):
        
        # create tweet
        self.assertTrue(client.login(username=self.user1_name, password=self.user1_pass))
        response = client.post(
            self.apiurl,
            data=self.valid_tweet,
            content_type=self.content_type
        )
        tweet_id = response.data['id']
        client.logout()

        # delete tweet
        response = client.delete(
            "%s%d/" % (self.apiurl, tweet_id),
            data=json.dumps({"text": "something else"}),
            content_type=self.content_type
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
