from django.contrib import admin
from .models import FoodItems,Activities,FoodRoutine

# Register your models here.


admin.site.register(Activities)
admin.site.register(FoodRoutine)

@admin.register(FoodItems)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['food','caloire','tag_list']
    
    def get_queryset(self, request):
        print(super().get_queryset(request).prefetch_related('tags'))
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())