from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from .contest_event_model import Event

User = get_user_model()

class EventRegistration(models.Model):
    """
    Base model for all event registrations
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    registered_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    feedback = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('event', 'user')
        
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"