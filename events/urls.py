from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('', views.home, name="home"),
    path('events/', views.events, name="events"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path("events/info/<int:event_id>/", views.event_detail, name="event_detail"),

    path("login/", views.login_profile, name="login_profile"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("register/", views.register_profile, name="register_profile"),

    path("event/register/<int:event_id>/", views.student_event_register, name="student_event_register"),
    path("event/register/success/", views.success_page, name="success_page"), 

    path("create/", views.create_event, name="create_event" ),
    path("event/<int:event_id>/edit/", views.edit_event, name="edit_event"),
    path("event/<int:event_id>/delete/", views.delete_event, name="delete_event"),
    path("event/<int:event_id>/participants/", views.event_participants, name="event_participants"),
    
    path("about/", views.about_creators, name="about_creators"),
]
