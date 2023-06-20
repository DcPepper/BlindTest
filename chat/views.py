from django.shortcuts import render
import os
from django.shortcuts import render, redirect
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def index(request):
    return render(request, "chat/index.html")

def room(request, room_name):
    liste_music = ["media/"+e for e in os.listdir("media")]
    print(liste_music)
    return render(request, "chat/room.html", {"room_name": room_name, "musics":liste_music[0]})