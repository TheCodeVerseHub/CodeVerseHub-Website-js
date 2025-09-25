import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codeversehub.settings")
django.setup()

from main.models import Testimonial

# Create sample testimonials
testimonials = [
    {
        "name": "Alex Johnson",
        "role": "Software Developer",
        "content": "CodeVerseHub's Discord server has been an amazing resource for my coding journey. The community is incredibly supportive and knowledgeable!",
        "is_active": True
    },
    {
        "name": "Sarah Williams",
        "role": "CS Student",
        "content": "I joined this Discord server as a beginner programmer, and it's been instrumental in my growth. Everyone is so helpful and welcoming.",
        "is_active": True
    },
    {
        "name": "Michael Chen",
        "role": "Full-stack Developer",
        "content": "The resources shared in this community are top-notch. I've learned so much from the discussions and code reviews from experienced developers.",
        "is_active": True
    }
]

# Add testimonials to database
for testimonial_data in testimonials:
    Testimonial.objects.create(**testimonial_data)

print("Sample testimonials added successfully!")