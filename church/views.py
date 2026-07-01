from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BibleVerse, Announcement, PrayerRequest
import random

@login_required(login_url='/login/')
def dashboard_view(request):
    verse_count = BibleVerse.objects.count()
    if verse_count > 0:
        random_index = random.randint(0, verse_count - 1)
        verse = BibleVerse.objects.all()[random_index]
    else:
        verse = None
    announcements = Announcement.objects.order_by('-created_at')[:3]
    context = {
        'verse': verse,
        'announcements': announcements,
    }
    return render(request, 'church/dashboard.html', context)

@login_required(login_url='/login/')
def prayer_view(request):
    if request.method == 'POST':
        message = request.POST['message']
        if message.strip():
            PrayerRequest.objects.create(
                member=request.user,
                message=message
            )
            messages.success(request, 'Your prayer request has been submitted! 🙏')
            return redirect('/prayer/')
    prayers = PrayerRequest.objects.filter(
        member=request.user
    ).order_by('-created_at')
    return render(request, 'church/prayer.html', {'prayers': prayers})

@login_required(login_url='/login/')
def announcements_view(request):
    announcements = Announcement.objects.order_by('-created_at')
    return render(request, 'church/announcements.html', {'announcements': announcements})