from django.test import TestCase, Client
from django.urls import reverse
from api.models import DBSongs, DBUserQueries
from django.contrib.auth.models import User

class TestViews(TestCase):
    def test_create_user(self):
        client = Client()
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = client.post(reverse('usercreate'),data)
        self.assertEqual(response.status_code, 201)


    def test_login(self):
        client = Client()
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = client.post(reverse('usercreate'),data)
        response = client.post(reverse('userlogin'),data)
        self.assertEqual(response.status_code, 200)


    def test_get_songs(self):
        DBSongs.objects.create(
            song_name='dont blame me',
            artist_name='Taylor Swift'
        )
        client = Client()
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = client.post(reverse('usercreate'),data)
        response = client.post(reverse('userlogin'),data)
        headers = {'Authorization': f'Bearer {response.data["access"]}', 
          'Content-Type': 'application/json',}
        data = {'songsDescription': 'give me a song by Taylor Swift now'}
        response = client.post(reverse('usersongs'),data,**headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'songs_list': [{'song': 'dont blame me'}]})


    def test_userqueries_songs(self):
        DBSongs.objects.create(
            song_name='dont blame me',
            artist_name='Taylor Swift'
        )
        DBUserQueries.objects.create(data=[{'song': 'dont blame me'}],
                                     user=User.objects.create_user(username='testuser', password='testpassword'),
                                     description='give me a song by Taylor Swift now')
        client = Client()
        response = client.get(reverse('userqueries'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'query_list': [{'description': 'give me a song by Taylor Swift now'}]})
        
