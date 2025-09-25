from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path("", views.home, name="home"),
    
    # Static pages - Discord server information
    path("resources/", views.resources_view, name="resources"),
    path("timeline/", views.timeline_view, name="timeline"),
    path("rules/", views.rules_view, name="rules"),
    path("faq/", views.faq_view, name="faq"),
    path("about/", views.about_view, name="about"),
    path("contact/", views.contact_view, name="contact"),
]
