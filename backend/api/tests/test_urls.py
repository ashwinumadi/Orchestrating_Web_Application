from django.test import SimpleTestCase
from django.urls import reverse, resolve
from api.views import  CreateUserView, Login, GetSongs, LogoutView, UserQueries

class TestUrls(SimpleTestCase):

    def test_userlogin_url_is_resolved(self):
        url = reverse('userlogin')
        self.assertEquals(resolve(url).func.view_class, Login)
    
    def test_usercreate_url_is_resolved(self):
        url = reverse('usercreate')
        self.assertEquals(resolve(url).func.view_class, CreateUserView)
    
    def test_usersongs_url_is_resolved(self):
        url = reverse('usersongs')
        self.assertEquals(resolve(url).func.view_class, GetSongs)
    
    def test_userlogout_url_is_resolved(self):
        url = reverse('userlogout')
        self.assertEquals(resolve(url).func.view_class, LogoutView)
    
    def test_userqueries_url_is_resolved(self):
        url = reverse('userqueries')
        self.assertEquals(resolve(url).func.view_class, UserQueries)
