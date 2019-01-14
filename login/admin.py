from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.User)
admin.site.register(models.Class)
admin.site.register(models.Course)
admin.site.register(models.Time)
admin.site.register(models.Score)
admin.site.register(models.Prerequisite)
admin.site.register(models.Department)