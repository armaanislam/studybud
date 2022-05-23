from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name #Without setting this, Topic name will be shown as "Topic object" in admin database

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) #Someone will host a topic
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) #A topic can have multiple rooms, a room can have multiple topics but for now a room can have only one topic
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) #Blank = form, null = database; True means, wihtout any value the model can have this instance
    participants = models.ManyToManyField(User, related_name='participants', blank=True) #As the user model is already onnected with room hot, we need to spcify a related name for this user
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created'] #Newest upda te will be shown first

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField() #() blank means the user is forced to type a message in the field
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50] #If its a long message, it will show only the first 50 words