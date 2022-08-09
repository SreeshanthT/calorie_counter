from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter() 
router.register(r'food-item', views.FoodItemViewSet)

urlpatterns = [
    path('',include([
        path('',views.index,name='index'), 
    ])),
    path('', include(router.urls)),
    
    path('register/',views.RegisterView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login')
]