from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.models import Count
from django.utils import timezone
from .models import JournalEntry, JournalImage, Topic
from .forms import JournalEntryForm, TopicForm
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
        year = int(self.request.GET.get('year', today.year))
        month = int(self.request.GET.get('month', today.month))
        
        # Handle month wrap-around
        if month > 12:
            month = 1
            year += 1
        elif month < 1:
            month = 12
            year -= 1
            
        # Calculate navigation links
        prev_month = month - 1
        prev_year = year
        if prev_month < 1:
            prev_month = 12
            prev_year -= 1
            
        next_month = month + 1
        next_year = year
        if next_month > 12:
            next_month = 1
            next_year += 1
        
        # Analytics: Mood distribution
        mood_data = JournalEntry.objects.values('mood').annotate(count=Count('mood'))
        mood_labels = [item['mood'].capitalize() for item in mood_data]
        mood_counts = [item['count'] for item in mood_data]
        
        # Analytics: Entry frequency (days with entries)
        total_entries = JournalEntry.objects.count()
        
        # Calendar logic: Only current month days
        import calendar
        cal = calendar.Calendar(firstweekday=6)
        # Get all days in the weeks that contain the month, then filter for current month
        all_days = [day for week in cal.monthdatescalendar(year, month) for day in week if day.month == month]
        
        # Map entries to dates for the calendar
        entries_by_date = {entry.date: entry for entry in JournalEntry.objects.all()}
        
        context.update({
            'mood_labels_json': json.dumps(mood_labels),
            'mood_counts_json': json.dumps(mood_counts),
            'total_entries': total_entries,
            'month_days': all_days,
            'entries_by_date': entries_by_date,
            'current_year': year,
            'current_month': month,
            'prev_month': prev_month,
            'prev_year': prev_year,
            'next_month': next_month,
            'next_year': next_year,
            'today': today,
            'view_date': datetime.date(year, month, 1),
        })
        return context

class EntryCreateView(CreateView):
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'journal/entry/entry_form.html'
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        date_str = request.GET.get('date')
        if date_str:
            try:
                date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                existing_entry = JournalEntry.objects.filter(date=date_obj).first()
                if existing_entry:
                    return redirect('entry_update', pk=existing_entry.pk)
            except ValueError:
                pass
        else:
            # Check for today if no date is specified
            today = timezone.now().date()
            existing_entry = JournalEntry.objects.filter(date=today).first()
            if existing_entry:
                return redirect('entry_update', pk=existing_entry.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        date_str = self.request.GET.get('date')
        if date_str:
            initial['date'] = date_str
        else:
            initial['date'] = timezone.now().date()
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        images = self.request.FILES.getlist('images')
        for img in images:
            JournalImage.objects.create(entry=self.object, image=img)
        return response

class EntryUpdateView(UpdateView):
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'journal/entry/entry_form.html'
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
    template_name = 'journal/entry/entry_confirm_delete.html'

class EntryDetailView(DetailView):
    model = JournalEntry
    template_name = 'journal/entry/entry_detail.html'
    context_object_name = 'entry'

# i added 
class TopicDetailView(DetailView):
    model = Topic
    template_name = 'journal/topic/topic_detail.html'
    context_object_name = 'topic'

class TopicListView(ListView):
    model = Topic
    template_name = 'journal/topic/topic_list.html'
    context_object_name = 'topics'

class TopicCreateView(CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'journal/topic/topic_form.html'
    success_url = reverse_lazy('topic_list')

class TopicUpdateView(UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = 'journal/topic/topic_form.html'
    success_url = reverse_lazy('topic_list')

class TopicDeleteView(DeleteView):
    model = Topic
    template_name = 'journal/topic/topic_confirm_delete.html'
    success_url = reverse_lazy('topic_list')


