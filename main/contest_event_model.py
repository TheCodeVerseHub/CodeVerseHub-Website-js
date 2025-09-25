from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# Event base model
class Event(models.Model):
    """
    Base Event model for all event types
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True, help_text="Physical location or 'Online'")
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured_image = models.ImageField(upload_to='event_images', blank=True, null=True)
    max_participants = models.IntegerField(default=0, help_text="0 means unlimited")
    
    def __str__(self):
        return self.title
        
    @property
    def is_upcoming(self):
        return self.start_time > timezone.now()
        
    @property
    def is_ongoing(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time
        
    @property
    def is_past(self):
        return self.end_time < timezone.now()
        
    @property
    def status(self):
        if self.is_upcoming:
            return 'upcoming'
        elif self.is_ongoing:
            return 'ongoing'
        else:
            return 'completed'

# Create a ContestEvent model to extend the Event model with contest-specific attributes
class ContestEvent(models.Model):
    """
    ContestEvent model extends the Event model with contest-specific attributes
    """
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='contest_details')
    
    TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('team', 'Team'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    contest_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='individual')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium')
    rules = models.TextField(blank=True, help_text="Specific rules for this contest")
    resources_link = models.URLField(blank=True, help_text="Link to additional resources for the contest")
    team_size = models.IntegerField(default=1, help_text="Maximum team size (1 for individual contests)")
    
    def __str__(self):
        return f"Contest: {self.event.title}"
    
    @property
    def participants(self):
        from .models import ContestParticipant
        return ContestParticipant.objects.filter(contest_event=self)
    
    def get_participant_count(self):
        """Get the number of participants in this contest"""
        return self.participants.count()
    
    @property
    def participant_count(self):
        return self.get_participant_count()