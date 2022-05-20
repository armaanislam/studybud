from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm

#rooms = [
#    {'id': 1, 'name':'Lets learn python!'},
#    {'id': 2, 'name':'Design with me'},
#    {'id': 3, 'name':'Frontend Developers'},
#]

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | #q = search parameter
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count':room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    #room = None
    #for i in rooms:
    #    if i['id'] == int(pk):
    #        room = i
    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm() #calling RoomForm from above
    if request.method == 'POST': #To check if anyone sent any data
        form = RoomForm(request.POST) #Pass the data in form
        if form.is_valid(): #To check if the form is filled with data
            form.save() #To save the form
            return redirect('home') #After submission it will redirect to home; here we used name='home'
        #request.POST.get('name')
        #print(request.POST)

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})