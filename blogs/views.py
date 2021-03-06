from django.shortcuts import render, get_object_or_404
from rest_framework import generics, response, status, permissions
from .serializers import BlogSerializer, UserSerializer, LoginSerializer
from .models import Blog
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from knox.auth import TokenAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from knox.models import AuthToken
from  django.http import HttpResponse
import json
from rest_framework.authtoken.models import Token

class BlogCreate(generics.CreateAPIView):
  # permission_classes = (IsAuthenticated,)
  # authentication_classes = (TokenAuthentication,)
  queryset = ''
  # def get(self, request, *args, **kwargs):
  #   if request.user.is_authenticated:
  #     blogs = Blog.objects.filter(created_by=request.user)
  #     data = BlogSerializer(blogs, many=True).data
  #     return response.Response(data)
  #   else:
  #     return response.Response({'error': True, 'msg': 'Not signed in.'})
  serializer_class = BlogSerializer
  
  def post(self, request):
    request.data['created_by'] = request.user.pk
    super().post(request)
    return response.Response({'error': False, 'msg': 'Successfully created blog.'})

class BlogsList(generics.ListAPIView):
  permission_classes = (IsAuthenticated,)
  authentication_classes = (TokenAuthentication,)
  queryset = ''
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      blogs = Blog.objects.filter(created_by=request.user)
      data = BlogSerializer(blogs, many=True).data
      return response.Response(data)
    else:
      return response.Response({'error': True, 'msg': 'Not signed in.'})

class BlogDestroy(generics.DestroyAPIView):
  permission_classes = (IsAuthenticated,)
  authentication_classes = (TokenAuthentication,)
  queryset = ''
  serializer_class = BlogSerializer

  def delete(self, request):
    if get_object_or_404(Blog, pk=request.data['id']).delete():
      return response.Response({'status': True, 'msg': 'Blog deleted'})
    else:
      return response.Response({'status': False, 'msg': 'Blog not deleted'})


class BlogDetail(APIView):
  permission_classes = (TokenAuthentication,)
  queryset = ''
  serializer_class = BlogSerializer
  def get(self, request, blog_id):
    if request.user.is_authenticated:
      blog = Blog.objects.get(pk=blog_id)
      data = BlogSerializer(blog).data
      return response.Response(data)
    else:
      return response.Response({'error': True, 'msg': 'Not signed in.'})


class UserCreate(generics.CreateAPIView):
  permission_classes = ()
  authentication_classes = ()
  serializer_class = UserSerializer

class LoginView(generics.GenericAPIView):
  permission_classes = ()
  serializer_class = LoginSerializer
  def post(self, request,):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    if user:
      token = f'Token {AuthToken.objects.create(user)[1]}'
      return response.Response({'token': token}, status=status.HTTP_201_CREATED)
    else: 
      return response.Response({'error': True}, status=status.HTTP_400_BAD_REQUEST)

class UserAPI(generics.RetrieveAPIView):
  permission_classes = [
    permissions.IsAuthenticated,
  ]
  serializer_class = UserSerializer

  def get_object(self):
    return self.request.user 

# Add register view for users and view for return token authentication
# class RegisterView(generics.A)

# class User(APIView):
#   def get(self, request):
#     print(request)

class AuthUser(APIView):
  permission_classes = (IsAuthenticated,)
  authentication_classes = (TokenAuthentication,)
  def get(self, request):
    if request.user.is_authenticated:
      return response.Response({'userSession': True, 'msg': 'Session valid'}, status=status.HTTP_200_OK)
