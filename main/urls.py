from django.urls import path
from . import views

urlpatterns = [
    # Home and authentication
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard and profile
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/<str:username>/', views.profile_view, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # Contests
    path('contests/', views.contests_view, name='contests'),
    path('contests/<int:contest_id>/', views.contest_detail, name='contest_detail'),
    path('contests/<int:contest_id>/register/', views.register_contest, name='register_contest'),
    path('contests/create/', views.create_contest, name='create_contest'),
    
    # Problems
    path('problems/', views.problems_view, name='problems'),
    path('problems/<int:problem_id>/', views.problem_detail, name='problem_detail'),
    path('problems/create/', views.create_problem, name='create_problem'),
    
    # Static pages
    path('resources/', views.resources_view, name='resources'),
    path('timeline/', views.timeline_view, name='timeline'),
    path('rules/', views.rules_view, name='rules'),
    path('faq/', views.faq_view, name='faq'),
    path('about/', views.about_view, name='about'),
]