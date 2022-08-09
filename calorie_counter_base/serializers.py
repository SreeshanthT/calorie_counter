from pyexpat import model
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from calorie_counter_base.models import FoodItems,FoodRoutine,ActivityRoutine,Activities


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user
    
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label="Username",write_only=True)
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Access denied: Invalid credentials'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
    
    
class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItems
        fields = ['pk','food','caloire','status'] 
        
        
        
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activities
        fields = ['pk','activity','calorie_burnout','status'] 
         
        
class FoodRoutienListSerializer(serializers.ModelSerializer):
    food_item = FoodItemSerializer()
    class Meta:
        model = FoodRoutine
        fields = ['food_item','created_on']
         
class FoodRoutienCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodRoutine
        fields = ['food_item','created_on']
        
    def validate(self, data):
        food_item = data['food_item']
        if food_item:
            if food_item.active == 1:
                return data
            else:
                raise serializers.ValidationError("Please select active food items")
        return data
        
        
class ActivityRoutineListSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()
    class Meta:
        model = ActivityRoutine
        fields = ['pk','activity','created_on','activity_status','start_time','end_time','activity_time']
        
class ActivityRoutineCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityRoutine
        fields = ['activity','created_on','status']
        
    def validate(self, data):
        activity = data['activity']
        if activity:
            if activity.active == 1:
                return data
            else:
                raise serializers.ValidationError("Please select active food items")
        return data
