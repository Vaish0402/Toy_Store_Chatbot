from django.urls import path
from . import views

urlpatterns = [
    path("", views.chatbot_view, name="chat"),
    path('upload/', views.upload_file, name='upload_file'),

]
