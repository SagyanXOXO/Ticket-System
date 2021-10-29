from django.urls import path
from .views import LoginView, RegisterView, HomeView, LogoutView, TicketListView, TicketView, NotificationView

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('tickets/', TicketListView.as_view(), name = 'ticket_list'),
    path('ticket/<int:id>', TicketView.as_view(), name = 'ticket'),
    path('notification/', NotificationView.as_view(), name = 'notification'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('register/', RegisterView.as_view(), name = 'register')
]