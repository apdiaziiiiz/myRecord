from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Count
from django.utils import timezone
from .models import JournalEntry, JournalImage
from .forms import JournalEntryForm
import datetime
import json

class DashboardView(ListView):
    model = JournalEntry
    template_name = 'journal/dashboard.html'
    context_object_name = 'entries'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        
        # Monthly filtering logic (default to current month)
        year = self.request.GET.get('year', today.year)
        month = self.request.GET.get('month', today.month)
        
        # Analytics: Mood distribution
        mood_data = JournalEntry.objects.values('mood').annotate(count=Count('mood'))
        mood_labels = [item['mood'].capitalize() for item in mood_data]
        mood_counts = [item['count'] for item in mood_data]
        
        # Analytics: Entry frequency (days with entries)
        total_entries = JournalEntry.objects.count()
        
        # Calendar logic
        import calendar
        cal = calendar.Calendar(firstweekday=6)
        month_days = cal.monthdatescalendar(int(year), int(month))
        
        # Map entries to dates for the calendar
        entries_by_date = {entry.date: entry for entry in JournalEntry.objects.all()}
        
        context.update({
            'mood_labels_json': json.dumps(mood_labels),
            'mood_counts_json': json.dumps(mood_counts),
            'total_entries': total_entries,
            'month_days': month_days,
            'entries_by_date': entries_by_date,
            'current_year': int(year),
            'current_month': int(month),
            'today': today,
        })
        return context

class EntryCreateView(CreateView):
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'journal/entry_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        images = self.request.FILES.getlist('images')
        for img in images:
            JournalImage.objects.create(entry=self.object, image=img)
        return response

class EntryUpdateView(UpdateView):
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'journal/entry_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        images = self.request.FILES.getlist('images')
        if images:
            # Optionally clear old images or just add new ones
            # For this simple app, we just add more
            for img in images:
                JournalImage.objects.create(entry=self.object, image=img)
        return response

class EntryDeleteView(DeleteView):
    model = JournalEntry
    success_url = reverse_lazy('dashboard')
    template_name = 'journal/entry_confirm_delete.html'

class EntryDetailView(DetailView):
    model = JournalEntry
    template_name = 'journal/entry_detail.html'
    context_object_name = 'entry'
