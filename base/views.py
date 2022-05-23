from django.shortcuts import render, redirect
from django.contrib import messages #Flash messages; these are stored in django sessions; stored inside for a one browser refresh
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm

#rooms = [
#    {'id': 1, 'name':'Lets learn python!'},
#    {'id': 2, 'name':'Design with me'},
#    {'id': 3, 'name':'Frontend Developers'},
#]

def loginPage(request): #Django has a built in function named login, so we can't use that
    page = 'login'
    if request.user.is_authenticated: #Means if the user logs in, and through url he goes back to the login page, he will be redirected to home that is the dont need to login again
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower() #we user name = 'username' in input in navbar.html
        password = request.POST.get('password')

        try: #To authenticate if the user exists
            user = User.objects.filter(username=username)
            user.user
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password) #Django user authentication; if we delete the session token from cookies, it will logout the user from site.
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)



def logoutUser(request):
    logout(request)
    return redirect('home')



def registerPage(request):
    #page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #To access the user rightaway, so commit=False to get that user object
            user.name = user.username.lower()
            user.save()
            login(request, user) #Let the user login then redirect to home page
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'base/login_register.html', {'form':form})



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | #q = search parameter
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    #room_messages = Message.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)) #Message_room_topic_name; If users clicks javascript in browse topic, only javascript related activited in recent activity
    context = {'rooms': rooms, 'topics': topics, 'room_count':room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)



def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()#.order_by('-created') #We can query child objects of a specific room; Room = parent, Message = Child, we have lowercase child name
    participants = room.participants.all() # One to many relation: _set.all(); Many to many relation: .all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id) #####

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all() #To get all children of a specific object, modelname_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login') #Extra authentication, To check if the user session does not exist, it will redirect to login page
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



@login_required(login_url='login') #Extra authentication
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host: #Only the owner of the room can update the row,
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html', context)



@login_required(login_url='login') #Extra authentication
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host: #Only the owner of the room can delete the row,
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})



@login_required(login_url='login') #Extra authentication
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user: #Only the owner of the room can delete the row,
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message}) #{'obj': message} making the html dynamic