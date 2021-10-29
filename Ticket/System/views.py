from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm, LoginForm, TicketForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Ticket, Notification
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


"""

This view is created just for handling AJAX
Used to fetch notifications and other notification properties such as notification count

"""
class NotificationView(View):
    def get(self, request):
        if request.is_ajax():
            action = request.GET.get('action')
            if action == 'get_notification':
                notification = Notification.objects.filter(user = request.user)

                notification = json.loads(serialize('json', notification))
                return JsonResponse({'notification' : notification})

            elif action == 'get_notification_count':
                notification_count = Notification.objects.filter(user = request.user, viewed = False).count()

                return JsonResponse({'notification_count' : notification_count})

            else:
                return redirect('/')    

    def post(self, request):
        if request.is_ajax():
            action = request.POST.get('action')
            if action == 'set_notification_viewed':
                return JsonResponse({'message' : 'success'})  
                             


"""

Basic login view to render a form for login and authenticate to log in users

"""
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        form = LoginForm()
        context = {'form' : form}
        return render(request, 'login.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username = username, password = password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'login.html', {'message' : 'Invalid credentials'})      


"""

Logs out current user in session and redirects them to the login page

"""
class LogoutView(View):
    def get(self, request):
        logout(request)

        return redirect('/login/')


"""

View for handling new user registrations
Logs in user automatically after successful registration

"""
class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        context = {'form' : form}
        return render(request, 'register.html', context)  

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']  
            user = authenticate(request, username = username, password = password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'login.html')    

        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            form = RegisterForm()
            return render (request, "register.html", {"form":form})


"""

This View is the Homepage where registered users can use to create a new ticket 
Users can also view notifications in real-time

"""
class HomeView(View):
    def get(self, request):
        form = TicketForm()
        return render(request, 'index.html', {'form' : form})   

    def post(self, request):
        subject = request.POST.get('subject')
        description = request.POST.get('description')

        print(subject, description)

        ticket = Ticket(
            user = request.user,
            subject = subject,
            description = description
        )

        ticket.save()

        return redirect('/')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)    

"""

Users can view all their tickets with their timestamps
Clicking on any particular ticket will open a detail view of that particular ticket
Ordering of the tickets in the list is from date Newest to Oldest

"""
class TicketListView(View):
    def get(self, request):
        tickets = Ticket.objects.filter(user = request.user)
        context = {'tickets' : tickets}
        return render(request, 'ticket_list.html', context) 

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)   

        
"""

Users can check detailed view of their tickets
Any comments made by admins regarding the ticket will be made visible with their respective timestamps

"""
class TicketView(View):
    def get(self, request, id):
        try:
            ticket = Ticket.objects.get(id = id, user = request.user) 
        except ObjectDoesNotExist:
            context = {}
        else:
            context = {'ticket' : ticket}

        return render(request, 'ticket.html', context)

    @method_decorator(login_required)        
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)        
                                



