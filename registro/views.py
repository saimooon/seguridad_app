# En views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from .forms import UserMessageForm
from .models import UserMessage, CustomUser
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


def manage_messages(request, message_id=None):
    # Get all user's messages
    user_messages = UserMessage.objects.filter(user=request.user)

    # If message_id is provided, fetch the specific message for editing or deletion
    message = get_object_or_404(UserMessage, id=message_id, user=request.user) if message_id else None

    # Handle the form for creating or modifying messages
    if request.method == 'POST':
        message_form = UserMessageForm(request.POST, instance=message) if message else UserMessageForm(request.POST)

        if 'create' in request.POST or 'modify' in request.POST:
            if message_form.is_valid():
                new_message = message_form.save(commit=False)
                new_message.user = request.user
                new_message.save()
                action_message = 'Mensaje enviado con éxito.' if 'create' in request.POST else 'Mensaje modificado con éxito.'
                messages.success(request, action_message)
                return HttpResponseRedirect(reverse('home'))

        elif 'delete' in request.POST:
            if message:
                message.delete()
                messages.success(request, 'Mensaje eliminado con éxito.')
                return redirect('home')

    else:
        # If message_id is present, it's an edit, so populate the form with the message data
        message_form = UserMessageForm(instance=message) if message else UserMessageForm()

    return render(request, 'home.html', {'user_messages': user_messages, 'message_form': message_form, 'editing_message': message})


def logout_view(request):
    logout(request)
    return redirect('home') 

@login_required
def home(request):
    username = request.user.username

    # Get only the messages of the current user
    user_messages = UserMessage.objects.filter(user=request.user)

    # Handle the form for creating messages for both GET and POST requests
    if request.method == 'POST':
        message_form = UserMessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.user = request.user
            message.save()
            messages.success(request, 'Mensaje enviado con éxito.')
            return HttpResponseRedirect(reverse('home'))
    else:
        # If it's a GET request or form is not valid, create a new form
        message_form = UserMessageForm()

    return render(request, 'home.html', {'username': username, 'user_messages': user_messages, 'message_form': message_form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')

            # Verificar si el nombre de usuario ya existe
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya está en uso. Por favor, elige otro.')
                return render(request, 'signup.html', {'form': form})

            user = form.save()
            password = form.cleaned_data.get('password1')

            # Try authenticating the user after signup
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Authentication failed after signup.')
        else:
            # Manejar mensajes de error personalizados para campos específicos
            if 'username' in form.errors:
                messages.error(request, 'El nombre de usuario ya está en uso. Por favor, elige otro.')
            elif 'password2' in form.errors:
                messages.error(request, 'Las contraseñas no coinciden o son demasiado comunes. Por favor, inténtalo de nuevo.')

            return render(request, 'signup.html', {'form': form})
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Obtiene el valor de 'next' de la solicitud (si está presente)
            next_url = request.GET.get('next', 'home')

            return redirect(next_url)  # Redirige a la URL proporcionada en 'next' o a la página de inicio por defecto
        else:
            # Manejar mensajes de error personalizados en la vista
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, f"{error}")
                    else:
                        messages.error(request, f"{field.capitalize()}: {error}")

            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
