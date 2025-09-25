from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

# Import necessary models
from .models import Announcement, Testimonial, ContactMessage
from .forms import ContactForm

def home(request):
    """Home page with Discord server information"""
    
    # Display announcements, testimonials, and handle contact form
    recent_announcements = Announcement.objects.filter(is_active=True)[:3]
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, "Thank you for your message! We'll get back to you soon.")
            return redirect('home')
    else:
        contact_form = ContactForm()
    
    context = {
        "discord_members": 450,  # You can adjust these static values or make them dynamic
        "discord_channels": 10,
        "discord_bots": 5,
        "recent_announcements": recent_announcements,
        "testimonials": testimonials,
        "contact_form": contact_form,
    }
    
    return render(request, "main/home.html", context)


# Static pages - only keep these
def resources_view(request):
    return render(request, "main/resources.html")


def timeline_view(request):
    return render(request, "main/timeline.html")


def rules_view(request):
    return render(request, "main/rules.html")


def faq_view(request):
    return render(request, "main/faq.html")


def about_view(request):
    return render(request, "main/about.html")


def testimonials_view(request):
    """Display all testimonials"""
    testimonials = Testimonial.objects.filter(is_active=True)
    return render(request, "main/home.html", {"testimonials": testimonials})


def contact_view(request):
    """Contact form page"""
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, "Thank you for your message! We'll get back to you soon.")
            return redirect('home')
    else:
        contact_form = ContactForm()
    
    return render(request, "main/home.html", {"contact_form": contact_form})
