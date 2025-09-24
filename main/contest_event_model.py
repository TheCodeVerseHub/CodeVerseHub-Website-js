from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# Create a ContestEvent model to extend the Event model with contest-specific attributes
class ContestEvent(models.Model):
    """
    ContestEvent model extends the Event model with contest-specific attributes
    """
    event = models.OneToOneField('Event', on_delete=models.CASCADE, related_name='contest_details')
    
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