from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter() 
router.register(r'food-item', views.FoodItemViewSet)
router.register(r'activity', views.ActivityViewSet)
 
urlpatterns = [

    path('',views.index,name='index'), 

    path('', include(router.urls)),
    
    path('register/',views.RegisterView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('food-routine-<str:pk>/',views.FoodRoutienView.as_view(),name='food-routine'),
    path('activity-routine-<str:pk>/',views.ActivityRoutineView.as_view(),name='activity-routine'),
    path('my-calorie-status/',views.MyCaloriesStatus.as_view(),name='my-calorie-status'),
    
]