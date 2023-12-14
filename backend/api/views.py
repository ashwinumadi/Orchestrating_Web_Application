from django.http import HttpResponse
from rest_framework import status, permissions
from .serializer import  UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.contrib.auth import authenticate, get_user_model
from .song_matching import song_matching, get_user_queries
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import  DBUserQueries
import os
import json
import redis
import logging


LOGGER = logging.getLogger()
logging.basicConfig(level=logging.INFO)


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer


class Login(APIView):
    def post(self, request, format=None):
        data = self.request.data
        if type(data) == str:
            data = json.loads(data)
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            refresh = RefreshToken.for_user(user)
            token = {'refresh': str(refresh), 'access': str(refresh.access_token)}
            return Response(token, status=status.HTTP_200_OK)
        else:
            response = HttpResponse('User not found.')
            response.status_code = 404  # sample status code
            return response


class GetSongs(APIView):
    def post(self, request, format=None):
        if self.request.user:
            if str(self.request.user)=='AnonymousUser':
                user = authenticate(username='testuser', password='testpassword')
            else:
                user = self.request.user
            description = self.request.data['songsDescription']
            #songs_list = song_matching(user, description)
            redisHost = os.getenv("REDIS_HOST") or "redis-service"
            redisPort = os.getenv("REDIS_PORT") or 6379
            REDIS_KEY = "toWorkers"
            r = redis.StrictRedis(host=redisHost, port=redisPort, db=0)
            count = r.lpush(REDIS_KEY,json.dumps(description))
            
            # Receiving the message from worker node
            REDIS_KEY = "fromWorkers"
            newdescription = r.blpop(REDIS_KEY)
            fetched_data = newdescription[1].decode('utf-8')
            
            output = json.loads(fetched_data)
            dbuserquery = DBUserQueries.objects.create(data=output['songs_list'],
                                                       user=user,
                                                       description=description)
            dbuserquery.save()
            return Response(output, status=status.HTTP_200_OK)
        else:
            return Response('User Not Found. First log in', status=status.HTTP_404_NOTFOUND)


class UserQueries(APIView):
    def get(self, request, format=None):
        if str(self.request.user)=='AnonymousUser':
            user = authenticate(username='testuser', password='testpassword')
        else:
            user = self.request.user
        if user:
            songs_list = get_user_queries(user)
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
