from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from .serializers import FoodItemSerializer, RegisterSerializer,LoginSerializer

from .models import FoodItems
# Create your views here.

def index(request):
    return HttpResponse('Done')
    

  

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    
class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)
    
class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItems.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.IsAuthenticated] 