from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth URLs
    path('', auth_views.LoginView.as_view(template_name='journal/auth/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('entry/new/', views.EntryCreateView.as_view(), name='entry_create'),
    path('entry/<int:pk>/', views.EntryDetailView.as_view(), name='entry_detail'),
    path('entry/<int:pk>/edit/', views.EntryUpdateView.as_view(), name='entry_update'),
    path('entry/<int:pk>/delete/', views.EntryDeleteView.as_view(), name='entry_delete'),
    
    path('topics/', views.TopicListView.as_view(), name='topic_list'),
    path('topics/new/', views.TopicCreateView.as_view(), name='topic_create'),
    path('topics/<int:pk>/edit/', views.TopicUpdateView.as_view(), name='topic_update'),
    path('topics/<int:pk>/delete/', views.TopicDeleteView.as_view(), name='topic_delete'),
    path('topics/<int:pk>/', views.TopicDetailView.as_view(), name='topic_detail'),
    
    # Autosave endpoints
    path('entry/autosave/', views.EntryAutosaveView.as_view(), name='entry_autosave'),
    path('topics/autosave/', views.TopicAutosaveView.as_view(), name='topic_autosave'),
]

