from django.contrib import admin
from .models import PrayerRequest, BibleVerse, Announcement, Attendance

admin.site.register(PrayerRequest)
admin.site.register(BibleVerse)
admin.site.register(Announcement)
admin.site.register(Attendance)