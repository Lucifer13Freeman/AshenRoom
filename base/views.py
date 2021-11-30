from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, UserCreationForm
from .apps import BaseConfig

# Create your views here.

app_name = BaseConfig.name

def login_page(request):

    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try: user = User.objects.get(email=email)
        except: messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else: messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, f'{app_name}/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_page(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else: messages.error(request, 'An error occurred during registration')

    return render(request, f'{app_name}/login_register.html', { 'form': form })


@login_required(login_url='login')
def user_profile(request, id):

    user = User.objects.get(id=id)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, f'{app_name}/profile.html', context)


def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''    

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()

    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]

    context = { 'rooms': rooms, 'topics': topics,
               'room_count': room_count, 
               'room_messages': room_messages }
    return render(request, f'{app_name}/home.html', context)


@login_required(login_url='login')
def room(request, id):

    room = Room.objects.get(id=id)
    room_messages = room.message_set.all()
    members = room.members.all()

    if request.method == 'POST':

        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )

        room.members.add(request.user)
        return redirect('room', id=room.id)

    context = { 'room': room, 
                'room_messages': room_messages,
                'members': members }
    return render(request, f'{app_name}/room.html', context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created_at = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            admin=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, f'{app_name}/room_form.html', context)


@login_required(login_url='login')
def update_room(request, id):

    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.admin:
        return HttpResponse('Your are not allowed here!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created_at = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')

        room.save()
        return redirect('home')

    context = { 'form': form, 'topics': topics, 'room': room }
    return render(request, f'{app_name}/room_form.html', context)


@login_required(login_url='login')
def delete_room(request, id):

    room = Room.objects.get(id=id)

    if request.user != room.admin:
        return HttpResponse('Your are not allowed here!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, f'{app_name}/delete.html', { 'obj': room })


@login_required(login_url='login')
def delete_message(request, id):

    message = Message.objects.get(id=id)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, f'{app_name}/delete.html', { 'obj': message })


@login_required(login_url='login')
def update_user(request):

    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
            form.save()
            return redirect('user-profile', id=user.id)

    return render(request, f'{app_name}/update-user.html', { 'form': form })


def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, f'{app_name}/topics.html', { 'topics': topics })


def activity_page(request):
    room_messages = Message.objects.all()
    return render(request, f'{app_name}/activity.html', { 'room_messages': room_messages })