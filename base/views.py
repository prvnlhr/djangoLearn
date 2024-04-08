from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room,Topic,User
from .forms import RoomForm



def loginPage(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exists')
        
        user = authenticate(request,username=username,password=password)  #check db for crendentials

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'username or password does not exists')

    return render(request, 'base/login_register_form.html')

def logoutUser(request):
    logout(request)
    return redirect('home')



def home(request):

    q = request.GET.get('q')
    
    key = q if q != None else ''

    rooms =Room.objects.filter(topic__name__contains=key)

    room_count  = rooms.count() # len(room)

    topics = Topic.objects.all()
    context = {'rooms':rooms,'topics':topics,'room_count':room_count}
    return render(request,'base/home.html',context)


def room(request,id):
    room = Room.objects.get(id=id)
    context ={'room':room}
    return render(request,'base/room.html',context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method =='POST':
        form =  RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form':form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')

def updateRoom(request,id):

    room = Room.objects.get(id=id)
    form =RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here !!')

    if request.method =='POST':
        form = RoomForm(request.POST, instance=room)  # for updating we pass instance of the room we need to update in DB, other wise it will create new rather then updating
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def deleteRoom(request,id):
    room = Room.objects.get(id=id)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here !!')
    
    if request.method =='POST':
        room.delete()
        return redirect('home')
    context = {'obj':room}
    return render(request,'base/delete.html',context)