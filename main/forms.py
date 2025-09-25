from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from .models import User, Contest, Problem, TestCase, Submission, ContactMessage


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    discord_username = forms.CharField(max_length=100, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'discord_username', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.discord_username = self.cleaned_data['discord_username']
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'location', 'website', 'discord_username', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid username or password.")
            if not user.is_active:
                raise forms.ValidationError("This account has been deactivated.")
        
        return self.cleaned_data


class ContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ['title', 'description', 'start_time', 'end_time', 'contest_type', 'difficulty', 'max_participants']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 6}),
        }


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'description', 'input_format', 'output_format', 'sample_input', 'sample_output', 'difficulty', 'tags', 'time_limit', 'memory_limit']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 8}),
            'input_format': forms.Textarea(attrs={'rows': 4}),
            'output_format': forms.Textarea(attrs={'rows': 4}),
            'sample_input': forms.Textarea(attrs={'rows': 4}),
            'sample_output': forms.Textarea(attrs={'rows': 4}),
        }


class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['input_data', 'expected_output', 'is_sample']
        widgets = {
            'input_data': forms.Textarea(attrs={'rows': 4}),
            'expected_output': forms.Textarea(attrs={'rows': 4}),
        }


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['code', 'language']
        widgets = {
            'code': forms.Textarea(attrs={'rows': 15, 'class': 'code-editor'}),
        }


class ContestFilterForm(forms.Form):
    STATUS_CHOICES = [('', 'All Status'), ('upcoming', 'Upcoming'), ('ongoing', 'Ongoing'), ('completed', 'Completed')]
    TYPE_CHOICES = [('', 'All Types')] + list(Contest.TYPE_CHOICES)
    DIFFICULTY_CHOICES = [('', 'All Difficulties')] + list(Contest.DIFFICULTY_CHOICES)
    
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    contest_type = forms.ChoiceField(choices=TYPE_CHOICES, required=False)
    difficulty = forms.ChoiceField(choices=DIFFICULTY_CHOICES, required=False)


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Your message...'}),
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject'}),
        }
