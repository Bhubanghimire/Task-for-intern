from django.contrib import admin
from .models import User,Task

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id','title','description','assigned']
    list_filter = ['status']