from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from PIL import Image
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models import QuerySet


class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Administrator'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    discord_username = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics', default='default.jpg')
    date_joined = models.DateTimeField(default=timezone.now)
    total_points = models.IntegerField(default=0)
    problems_solved = models.IntegerField(default=0)
    contests_participated = models.IntegerField(default=0)
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize profile picture
        try:
            img = Image.open(self.profile_picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_picture.path)
        except:
            pass
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_moderator(self):
        return self.role in ['admin', 'moderator']


class Contest(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    
    TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('team', 'Team'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    contest_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='individual')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium')
    max_participants = models.IntegerField(default=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_contests')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    @property
    def status(self):
        now = timezone.now()
        if now < self.start_time:
            return 'upcoming'
        elif now <= self.end_time:
            return 'ongoing'
        else:
            return 'completed'
    
    @property
    def duration_minutes(self):
        return int((self.end_time - self.start_time).total_seconds() / 60)
    
    def get_participant_count(self):
        """Get the number of participants in this contest"""
        return ContestParticipant.objects.filter(contest=self).count()
    
    @property
    def participant_count(self):
        return self.get_participant_count()


class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    input_format = models.TextField()
    output_format = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    tags = models.CharField(max_length=500, help_text="Comma-separated tags")
    time_limit = models.IntegerField(default=1000, help_text="Time limit in milliseconds")
    memory_limit = models.IntegerField(default=256, help_text="Memory limit in MB")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, null=True, blank=True, related_name='problems')
    
    def __str__(self):
        return self.title
    
    @property
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def get_submission_count(self):
        """Get the number of submissions for this problem"""
        return Submission.objects.filter(problem=self).count()
    
    def get_acceptance_rate(self):
        """Calculate the acceptance rate for this problem"""
        total = Submission.objects.filter(problem=self).count()
        if total == 0:
            return 0
        accepted = Submission.objects.filter(problem=self, verdict='accepted').count()
        return round((accepted / total) * 100, 2)
    
    @property
    def submission_count(self):
        return self.get_submission_count()
    
    @property
    def acceptance_rate(self):
        return self.get_acceptance_rate()


class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.TextField()
    is_sample = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Test case for {self.problem.title}"


class Submission(models.Model):
    VERDICT_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('wrong_answer', 'Wrong Answer'),
        ('time_limit_exceeded', 'Time Limit Exceeded'),
        ('memory_limit_exceeded', 'Memory Limit Exceeded'),
        ('runtime_error', 'Runtime Error'),
        ('compilation_error', 'Compilation Error'),
    ]
    
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('java', 'Java'),
        ('cpp', 'C++'),
        ('c', 'C'),
        ('javascript', 'JavaScript'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='submissions')
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, null=True, blank=True, related_name='submissions')
    code = models.TextField()
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    verdict = models.CharField(max_length=30, choices=VERDICT_CHOICES, default='pending')
    execution_time = models.IntegerField(null=True, blank=True)
    memory_used = models.IntegerField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.problem.title}"
    
    class Meta:
        ordering = ['-submitted_at']


class ContestParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contest_participations')
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='participants')
    registered_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    problems_solved = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'contest']
    
    def __str__(self):
        return f"{self.user.username} in {self.contest.title}"


class UserProblemStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    is_solved = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    first_solved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'problem']
    
    def __str__(self):
        return f"{self.user.username} - {self.problem.title}"


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
