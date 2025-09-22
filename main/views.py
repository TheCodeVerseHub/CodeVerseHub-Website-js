from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Contest, Problem, Submission, ContestParticipant, UserProblemStatus, Announcement, TestCase
from .forms import CustomUserCreationForm, LoginForm, UserProfileForm, ContestForm, ProblemForm, SubmissionForm, ProblemFilterForm, ContestFilterForm, TestCaseForm


def home(request):
    """Home page with platform statistics and featured content"""
    total_users = User.objects.count()
    total_contests = Contest.objects.count()
    total_problems = Problem.objects.filter(is_active=True).count()
    total_submissions = Submission.objects.count()
    
    upcoming_contests = Contest.objects.filter(
        start_time__gt=timezone.now(),
        is_active=True
    ).order_by('start_time')[:3]
    
    recent_announcements = Announcement.objects.filter(is_active=True)[:3]
    
    context = {
        'total_users': total_users,
        'total_contests': total_contests,
        'total_problems': total_problems,
        'total_submissions': total_submissions,
        'upcoming_contests': upcoming_contests,
        'recent_announcements': recent_announcements,
    }
    
    return render(request, 'main/home.html', context)


def register_view(request):
    """User registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'main/register.html', {'form': form})


def login_view(request):
    """User login"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
    else:
        form = LoginForm()
    
    return render(request, 'main/login.html', {'form': form})


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def dashboard(request):
    """User dashboard with personalized content"""
    user = request.user
    
    # User statistics
    user_submissions = Submission.objects.filter(user=user)
    solved_problems = UserProblemStatus.objects.filter(user=user, is_solved=True).count()
    total_submissions = user_submissions.count()
    accepted_submissions = user_submissions.filter(verdict='accepted').count()
    
    # Upcoming contests user is registered for
    upcoming_contests = Contest.objects.filter(
        participants__user=user,
        start_time__gt=timezone.now()
    ).order_by('start_time')[:3]
    
    # Recent submissions
    recent_submissions = user_submissions[:5]
    
    # Recommended problems (unsolved, similar difficulty)
    solved_problem_ids = UserProblemStatus.objects.filter(
        user=user, is_solved=True
    ).values_list('problem_id', flat=True)
    
    recommended_problems = Problem.objects.filter(
        is_active=True
    ).exclude(id__in=solved_problem_ids)[:5]
    
    context = {
        'solved_problems': solved_problems,
        'total_submissions': total_submissions,
        'accepted_submissions': accepted_submissions,
        'acceptance_rate': round((accepted_submissions/total_submissions*100) if total_submissions > 0 else 0, 2),
        'upcoming_contests': upcoming_contests,
        'recent_submissions': recent_submissions,
        'recommended_problems': recommended_problems,
    }
    
    return render(request, 'main/dashboard.html', context)


def contests_view(request):
    """Contest listing with filtering"""
    filter_form = ContestFilterForm(request.GET)
    contests = Contest.objects.filter(is_active=True)
    
    if filter_form.is_valid():
        status = filter_form.cleaned_data.get('status')
        contest_type = filter_form.cleaned_data.get('contest_type')
        difficulty = filter_form.cleaned_data.get('difficulty')
        
        if status:
            now = timezone.now()
            if status == 'upcoming':
                contests = contests.filter(start_time__gt=now)
            elif status == 'ongoing':
                contests = contests.filter(start_time__lte=now, end_time__gt=now)
            elif status == 'completed':
                contests = contests.filter(end_time__lte=now)
        
        if contest_type:
            contests = contests.filter(contest_type=contest_type)
        
        if difficulty:
            contests = contests.filter(difficulty=difficulty)
    
    contests = contests.order_by('start_time')
    
    paginator = Paginator(contests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
    }
    
    return render(request, 'main/contests.html', context)


def contest_detail(request, contest_id):
    """Contest detail view"""
    contest = get_object_or_404(Contest, id=contest_id, is_active=True)
    is_registered = False
    
    if request.user.is_authenticated:
        is_registered = ContestParticipant.objects.filter(
            user=request.user, contest=contest
        ).exists()
    
    problems = Problem.objects.filter(contest=contest, is_active=True)
    participants = ContestParticipant.objects.filter(contest=contest).order_by('-score', 'registered_at')[:10]
    
    context = {
        'contest': contest,
        'is_registered': is_registered,
        'problems': problems,
        'participants': participants,
    }
    
    return render(request, 'main/contest_detail.html', context)


@login_required
@require_POST
def register_contest(request, contest_id):
    """Register for a contest"""
    contest = get_object_or_404(Contest, id=contest_id, is_active=True)
    
    if contest.status != 'upcoming':
        messages.error(request, 'Registration is closed for this contest.')
        return redirect('contest_detail', contest_id=contest_id)
    
    if contest.participant_count >= contest.max_participants:
        messages.error(request, 'Contest is full.')
        return redirect('contest_detail', contest_id=contest_id)
    
    participant, created = ContestParticipant.objects.get_or_create(
        user=request.user, contest=contest
    )
    
    if created:
        messages.success(request, 'Successfully registered for the contest!')
    else:
        messages.info(request, 'You are already registered for this contest.')
    
    return redirect('contest_detail', contest_id=contest_id)


def problems_view(request):
    """Problem listing with filtering"""
    filter_form = ProblemFilterForm(request.GET)
    problems = Problem.objects.filter(is_active=True, contest__isnull=True)
    
    if request.user.is_authenticated:
        solved_problem_ids = UserProblemStatus.objects.filter(
            user=request.user, is_solved=True
        ).values_list('problem_id', flat=True)
    else:
        solved_problem_ids = []
    
    if filter_form.is_valid():
        difficulty = filter_form.cleaned_data.get('difficulty')
        tags = filter_form.cleaned_data.get('tags')
        solved = filter_form.cleaned_data.get('solved')
        
        if difficulty:
            problems = problems.filter(difficulty=difficulty)
        
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            for tag in tag_list:
                problems = problems.filter(tags__icontains=tag)
        
        if solved and request.user.is_authenticated:
            if solved == 'solved':
                problems = problems.filter(id__in=solved_problem_ids)
            elif solved == 'unsolved':
                problems = problems.exclude(id__in=solved_problem_ids)
    
    problems = problems.order_by('difficulty', 'title')
    
    paginator = Paginator(problems, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
        'solved_problem_ids': solved_problem_ids,
    }
    
    return render(request, 'main/problems.html', context)


def problem_detail(request, problem_id):
    """Problem detail and submission view"""
    problem = get_object_or_404(Problem, id=problem_id, is_active=True)
    
    user_status = None
    user_submissions = []
    
    if request.user.is_authenticated:
        user_status, _ = UserProblemStatus.objects.get_or_create(
            user=request.user, problem=problem
        )
        user_submissions = Submission.objects.filter(
            user=request.user, problem=problem
        ).order_by('-submitted_at')[:10]
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to submit solutions.')
            return redirect('login')
        
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.problem = problem
            submission.save()
            
            # Update user problem status
            if user_status:
                user_status.attempts += 1
                user_status.save()
            
            messages.success(request, 'Solution submitted successfully!')
            return redirect('problem_detail', problem_id=problem_id)
    else:
        form = SubmissionForm()
    
    context = {
        'problem': problem,
        'form': form,
        'user_status': user_status,
        'user_submissions': user_submissions,
    }
    
    return render(request, 'main/problem_detail.html', context)


@login_required
def profile_view(request, username=None):
    """User profile view"""
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user
    
    user_stats = {
        'problems_solved': UserProblemStatus.objects.filter(user=profile_user, is_solved=True).count(),
        'total_submissions': Submission.objects.filter(user=profile_user).count(),
        'contests_participated': ContestParticipant.objects.filter(user=profile_user).count(),
    }
    
    recent_submissions = Submission.objects.filter(user=profile_user)[:10]
    recent_contests = ContestParticipant.objects.filter(user=profile_user).order_by('-registered_at')[:5]
    
    context = {
        'profile_user': profile_user,
        'user_stats': user_stats,
        'recent_submissions': recent_submissions,
        'recent_contests': recent_contests,
        'is_own_profile': profile_user == request.user,
    }
    
    return render(request, 'main/profile.html', context)


@login_required
def edit_profile(request):
    """Edit user profile"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'main/edit_profile.html', {'form': form})


# Static pages
def resources_view(request):
    return render(request, 'main/resources.html')


def timeline_view(request):
    return render(request, 'main/timeline.html')


def rules_view(request):
    return render(request, 'main/rules.html')


def faq_view(request):
    return render(request, 'main/faq.html')


def about_view(request):
    return render(request, 'main/about.html')


# Admin/Moderator views
@login_required
def create_contest(request):
    """Create a new contest (moderators and admins only)"""
    if not request.user.is_moderator:
        messages.error(request, 'You do not have permission to create contests.')
        return redirect('contests')
    
    if request.method == 'POST':
        form = ContestForm(request.POST)
        if form.is_valid():
            contest = form.save(commit=False)
            contest.created_by = request.user
            contest.save()
            messages.success(request, 'Contest created successfully!')
            return redirect('contest_detail', contest_id=contest.id)
    else:
        form = ContestForm()
    
    return render(request, 'main/create_contest.html', {'form': form})


@login_required
def create_problem(request):
    """Create a new problem (moderators and admins only)"""
    if not request.user.is_moderator:
        messages.error(request, 'You do not have permission to create problems.')
        return redirect('problems')
    
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.created_by = request.user
            problem.save()
            messages.success(request, 'Problem created successfully!')
            return redirect('problem_detail', problem_id=problem.id)
    else:
        form = ProblemForm()
    
    return render(request, 'main/create_problem.html', {'form': form})
