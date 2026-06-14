from django.contrib import admin
from django.urls import path
from accounts import views as account_views
from church import views as church_views
from chatbot import views as chatbot_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', account_views.login_view, name='login'),
    path('register/', account_views.register_view, name='register'),
    path('logout/', account_views.logout_view, name='logout'),
    path('dashboard/', church_views.dashboard_view, name='dashboard'),
    path('prayer/', church_views.prayer_view, name='prayer'),
    path('announcements/', church_views.announcements_view, name='announcements'),
    path('chatbot/', chatbot_views.chatbot_view, name='chatbot'),
    path('chatbot/message/', chatbot_views.chatbot_message, name='chatbot_message'),
]