from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('entry/new/', views.EntryCreateView.as_view(), name='entry_create'),
    path('entry/<int:pk>/', views.EntryDetailView.as_view(), name='entry_detail'),
    path('entry/<int:pk>/edit/', views.EntryUpdateView.as_view(), name='entry_update'),
    path('entry/<int:pk>/delete/', views.EntryDeleteView.as_view(), name='entry_delete'),
]
