from django.contrib import admin
from .models import Stage

admin.site.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ['stage', 'month', 'year']