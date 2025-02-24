from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages  # For error messages
from django.db import connection

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')  # ✅ Correct redirect
        else:
            messages.error(request, "Invalid registration details.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # ✅ Correct redirect
            else:
                form.add_error(None, "Invalid login credentials")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def home_page(request):
    query = request.GET.get('query', '')
    results = None
    if query:
        # 🚨 Vulnerable SQL Query: Directly concatenating user input!
        sql = "SELECT * FROM breachbuster_product WHERE name LIKE '%%{}%%'".format(query)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
    return render(request, 'home.html', {'results': results, 'query': query})
