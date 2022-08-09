from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

from taggit.managers import TaggableManager
from django_lifecycle import LifecycleModelMixin,hook,BEFORE_UPDATE


# Create your models here.
ACTIVE = 1
PENDING = 2
INACTIVE = 3

active_choices = (
        (INACTIVE, 'Inactive'),
        (ACTIVE, 'Active'),
        (PENDING, 'Pending'),
    )

class FoodItems(models.Model):
    food = models.CharField("Food Item",max_length=100,null=True)
    caloire = models.IntegerField("Calories")
    active = models.SmallIntegerField('Status', default=2, choices=active_choices)
    
    tags = TaggableManager()
    
    def get_tags(self):
        return u", ".join(o.name for o in self.tags.all())

    class Meta:
        verbose_name = "Food item"
        verbose_name_plural = "Food items"
        
    @property
    def status(self):
        return dict(active_choices)[self.active]
    
    

class Activities(models.Model):
    activity = models.CharField("Activity",max_length=100,null=True)
    calorie_burnout = models.IntegerField("Calorie Burnout")
    active = models.SmallIntegerField('Status', default=1, choices=active_choices)
    
    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        
    @property
    def status(self):
        return dict(active_choices)[self.active]
        
        
class FoodRoutine(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    food_item = models.ForeignKey(FoodItems,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    
    @property
    def food_routine(self):
        return self.__class__.objects.filter(created_on = self.created_on).values()

class ActivityRoutine(LifecycleModelMixin,models.Model):
    
    status_choices = (
        (1,'STARTED'),
        (2,'FINISHED') 
    )
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    activity = models.ForeignKey(Activities,on_delete=models.CASCADE)
    
    start_time = models.DateTimeField(null=True,blank=True)
    end_time = models.DateTimeField(null=True,blank=True)

    status = models.SmallIntegerField(null=True,choices=status_choices,blank=True)
    
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    
    @hook(BEFORE_UPDATE)
    def set_time(self):
        if self.status == 1:
            self.start_time = datetime.now()
        elif self.status == 2:
            self.end_time = datetime.now()

    @property
    def activity_status(self):
        if self.status:
            return dict(self.status_choices)[self.status]
        return "Not started yet"
    
    @property
    def activity_time(self):
        if self.start_time and self.end_time:
            return self.start_time - self.end_time
        return 'Not started yet' if self.start_time is None else 'Not finished yet'