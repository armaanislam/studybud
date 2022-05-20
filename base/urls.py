from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), #We can reference a view or a specific url using name
    path('room/<str:pk>/', views.room, name='room'), # room/ won't matter if we specify name
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
]