from django.urls import path
from .views import CreateUserView, Login, GetSongs, LogoutView, UserQueries

urlpatterns = [
    path('login/', Login.as_view(), name='user-login'),
    path('create-user/', CreateUserView.as_view()),
    path('get-songs', GetSongs.as_view()),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('get-user-queries/', UserQueries.as_view(), name='user-logout'),
]
