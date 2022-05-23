from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants'] #When we create a room, host and participation selection won't be shown

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']