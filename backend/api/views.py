from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status, permissions
from .serializer import  UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.contrib.auth import authenticate, get_user_model
from .song_matching import song_matching, get_user_queries
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
#from .serializer import UserRegistrationSerializer
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer


class Login(APIView):
    def post(self, request, format=None):
        data = self.request.data
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            refresh = RefreshToken.for_user(user)
            token = {'refresh': str(refresh), 'access': str(refresh.access_token)}
            print('Return Inside Login')
            return Response(token, status=status.HTTP_200_OK)
        else:
            print('Return Inside Login with error')
            response = HttpResponse('User not found. Ben stokes')
            response.status_code = 404  # sample status code
            return response


class GetSongs(APIView):
    def post(self, request, format=None):
        if self.request.user:
            description = self.request.data['songsDescription']
            songs_list = song_matching(self.request.user, description)
            return Response(songs_list, status=status.HTTP_200_OK)
        else:
            return Response('User Not Found. First log in', status=status.HTTP_404_NOTFOUND)

class UserQueries(APIView):
    def get(self, request, format=None):
        if self.request.user.is_authenticated:
            songs_list = get_user_queries(self.request.user)
            return Response(songs_list, status=status.HTTP_200_OK)
        else:
            return Response('User Not Found. First log in', status=status.HTTP_404_NOTFOUND)

class LogoutView(APIView):
    def post(self, request):
        if self.request.user.is_authenticated:
            user = request.user
            user.jti = None 
            user.save()
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'User not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
