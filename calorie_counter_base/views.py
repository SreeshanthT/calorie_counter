from datetime import timedelta
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login
from django.db.models import F,Sum

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


from calorie_counter_base.utils import get_object_or_none
from .serializers import FoodItemSerializer, RegisterSerializer,LoginSerializer,\
    FoodRoutienCreateSerializer,ActivityRoutineCreateSerializer,ActivitySerializer,ActivityRoutineListSerializer,\
    FoodRoutienListSerializer

from .models import FoodItems,FoodRoutine,ActivityRoutine,Activities
# Create your views here.

def index(request):
    return render(request,'index.html',locals())
    

  

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
class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activities.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated] 
    
    
    
class FoodRoutienView(views.APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        food_routine = get_object_or_none(FoodRoutine,id=kwargs.get('pk'))
        serializer = FoodRoutienListSerializer(
            instance=food_routine
        )
        
        if food_routine is None:
            qs = FoodRoutine.objects.filter(user=request.user)
            
            if request.GET.get('month'):
                qs = qs.filter(created_on__month=request.GET.get('month'))
            if request.GET.get('day'):
                qs = qs.filter(created_on__day=request.GET.get('day'))
            if request.GET.get('year'):
                qs = qs.filter(created_on__year=request.GET.get('year'))
                
                
            serializer = FoodRoutienListSerializer(qs,many=True)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    
    def post(self, request, *args, **kwargs):
        food_routine = get_object_or_none(FoodRoutine,id=kwargs.get('pk'))
        
        serializer = FoodRoutienCreateSerializer(
            data=self.request.data,
            instance=food_routine
        )
        if serializer.is_valid(raise_exception=True):
            obj = serializer.save()
            obj.user = request.user
            obj.save()

        return Response(serializer.data)
    
class ActivityRoutineView(views.APIView):
    # permission_classes = (permissions.AllowAny,)
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        activity_routine = get_object_or_none(ActivityRoutine,id=kwargs.get('pk'))
        serializer = ActivityRoutineListSerializer(instance=activity_routine)
        
        if activity_routine is None:
            
            qs = ActivityRoutine.objects.filter(user = request.user)
            
            if request.GET.get('month'):
                qs = qs.filter(created_on__month=request.GET.get('month'))
            if request.GET.get('day'):
                qs = qs.filter(created_on__day=request.GET.get('day'))
            if request.GET.get('year'):
                qs = qs.filter(created_on__year=request.GET.get('year'))
            
            serializer = ActivityRoutineListSerializer(qs,many=True)
        
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        activity_routine = get_object_or_none(ActivityRoutine,id=kwargs.get('pk'))
        
        serializer = ActivityRoutineCreateSerializer(
            data=self.request.data,
            instance=activity_routine
        )
        if serializer.is_valid(raise_exception=True):
            obj = serializer.save()
            obj.user = request.user
            obj.save()
            serializer = ActivityRoutineListSerializer(obj)
            

        return Response(serializer.data)
    
class MyCaloriesStatus(views.APIView):
    
    def get(self,request,*args,**kwargs):
        activity_routine = ActivityRoutine.objects.filter(user=request.user)
        food_routine = FoodRoutine.objects.filter(user=request.user)
        
        if request.GET.get('date_from') and request.GET.get('date_to'):
            activity_routine = activity_routine.filter(
                created_on__range=[request.GET.get('date_from'),request.GET.get('date_to')]
            )
            food_routine = food_routine.filter(
                created_on__range=[request.GET.get('date_from'),request.GET.get('date_to')]
            )
            
        if 'last_week' in request.GET:
            one_week_ago = datetime.datetime.today() - datetime.timedelta(days=7)
            
            activity_routine = activity_routine.filter(
                created_on__gte=one_week_ago
            )
            food_routine = food_routine.filter(
                created_on__gte=one_week_ago
            )
            
        if request.GET.get('month'):
            activity_routine = activity_routine.filter(
                created_on__month=request.GET.get('month')
            )
            food_routine = food_routine.filter(
                created_on__month=request.GET.get('month')
            )
            
        if request.GET.get('year'):
            activity_routine = activity_routine.filter(
                created_on__year=request.GET.get('year')
            )
            food_routine = food_routine.filter(
                created_on__year=request.GET.get('year')
            )
        

        response = {
            'burn_out':activity_routine.aggregate(Sum('activity__calorie_burnout'))['activity__calorie_burnout__sum'],
            'consumed':food_routine.aggregate(Sum('food_item__caloire'))['food_item__caloire__sum'],
            'activity_routine':ActivityRoutineListSerializer(activity_routine,many=True).data,
            'food_routine':FoodRoutienListSerializer(food_routine,many=True).data,
        }
        
        return Response(response)