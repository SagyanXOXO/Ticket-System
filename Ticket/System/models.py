from django.db import models
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

"""

Dropdown options for select for the Ticket model
Send notification to the user when status is closed

"""
status_choices = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Closed', 'Closed'),
    ('Ongoing', 'Ongoing'),
    ('Complete', 'Complete'),
)


"""

Ticket model, created by customers and can be edited by users
Override __init__ method to check for value of status before saving
If changed to closed, create Notification instance which in turn sends the notification signal
Checks if status choice has been changed from something other than closed for saving Notifications

"""
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    subject = models.CharField(max_length = 250)
    description = models.TextField()
    status = models.CharField(choices = status_choices, max_length = 9, default = 'Pending')
    progress = models.IntegerField(verbose_name = 'Progress Percentage', blank = True, null = True)
    remark = models.TextField(verbose_name = 'Closing Remarks', blank = True, null = True)
    created_on = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ['created_on']

    def __init__(self, *args, **kwargs):
        super(Ticket, self).__init__(*args, **kwargs)

        self.original_status = self.status.lower()    

    def save(self, *args, **kwargs):
        super(Ticket, self).save(*args, **kwargs)

        if self.status.lower() == 'closed':
            if self.original_status != self.status.lower():
                notification = Notification(
                    title = 'An admin closed your ticket' + " ' " + str(self.subject) + " ' " + 'created on' + " " + str(self.created_on),
                    user = self.user 
                )

                notification.save()

    def __str__(self):
        return str(self.subject)        


# Simple model to store comments from the admin on a particular ticket
class Comment(models.Model):
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)
    ticket = models.ForeignKey(Ticket, on_delete = models.CASCADE)    

    class Meta:
        ordering = ['-timestamp']    


"""

Set automatically when ticket status changed to closed
Save method overriding to send message through channel layers
When a notification is saved, sends the message to the channel group
Channel group name is the combination of the user in the notification model and their id seperated by an underscore
For eg : Ram_2

"""
class Notification(models.Model):
    title = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    viewed = models.BooleanField(default = False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return str(self.title)

    def __init__(self, *args, **kwargs):
        super(Notification, self).__init__(*args, **kwargs)

        if self.pk:
            self.exists = True
        else:
            self.exists = False     



    def save(self, *args, **kwargs):
        super(Notification, self).save(*args, **kwargs)   

        if not self.exists:
            channel_layer = get_channel_layer()
            message = str(self.title.capitalize())
            timestamp = str(self.timestamp)
            group_name = str(self.user.username) + '_' + str(self.user.id)
            async_to_sync(channel_layer.group_send)(
                group_name,
                    {
                        'type' : 'admin_notify',
                        'data' : json.dumps({
                            'message' : message,
                            'timestamp' : timestamp,
                        })
                    }
                )      



