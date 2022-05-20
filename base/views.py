from django.shortcuts import render, redirect
from django.contrib import messages #Flash messages; these are stored in django sessions; stored inside for a one browser refresh
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic
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

        try: #To authenticate if the user exists]
            user = User.objects.get(username=username)
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