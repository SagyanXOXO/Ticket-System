from django.contrib import admin
from .models import Ticket, Comment, Notification

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0 

class TicketAdmin(admin.ModelAdmin):
    inlines = [CommentInline]   

admin.site.register(Ticket, TicketAdmin)  

class NotificationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Notification, NotificationAdmin)

