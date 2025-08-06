from django.contrib import admin
from .models import ChatMessage


# Customize how ChatMessage is displayed in the admin panel
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("role", "message", "timestamp")     # Columns in admin list view
    list_filter = ("role", "timestamp")                 # Sidebar filters
    search_fields = ("message",)                        # Search bar
    ordering = ("-timestamp",)                          # Newest first
