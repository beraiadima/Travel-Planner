from django.contrib import admin
from .models import TravelProject, ProjectPlace




@admin.register(TravelProject)
class TravelProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_completed", "start_date", "created_at")
    list_filter = ("is_completed",)
    search_fields = ("name",)

@admin.register(ProjectPlace)
class ProjectPlaceAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "project", "is_visited", "created_at")
    list_filter = ("is_visited",)
    search_fields = ("title",)