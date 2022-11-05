from django.contrib import admin
from .models import *

# Register your models here.

class TasksAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

admin.site.register(Tasks, TasksAdmin)
