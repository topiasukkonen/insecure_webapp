import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import connection
from .models import Note
import subprocess

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('notes')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def notes(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        # Flaw 4: SQL Injection vulnerability
        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO vulnerable_app_note (user_id, title, content, created_at) VALUES ({request.user.id}, '{title}', '{content}', CURRENT_TIMESTAMP)")
    notes = Note.objects.filter(user=request.user)
    return render(request, 'notes.html', {'notes': notes})

@login_required
def system_info(request):
    info = {}
    error = None

    if request.method == 'POST':
        info_type = request.POST.get('info_type', '')
        # Flaw 5: Command Injection vulnerability
        try:
            if info_type == 'disk':
                command = "df -h"
            else:
                command = f"echo 'Unknown command: {info_type}'"
            
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            info[info_type] = output
        except subprocess.CalledProcessError as e:
            error = str(e.output)

    context = {
        'info': info,
        'error': error
    }
    return render(request, 'system_info.html', context)