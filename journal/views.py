from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from django.utils import timezone
from .models import JournalEntry, JournalImage, Topic
from .forms import JournalEntryForm, TopicForm
import datetime
import json

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'journal/auth/signup.html', {'form': form})

class DashboardView(LoginRequiredMixin, ListView):
    model = JournalEntry
    template_name = 'journal/dashboard.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

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
        
        user_entries = JournalEntry.objects.filter(user=self.request.user)
        
        # Analytics: Mood distribution
        mood_data = user_entries.values('mood').annotate(count=Count('mood'))
        mood_labels = [item['mood'].capitalize() for item in mood_data]
        mood_counts = [item['count'] for item in mood_data]
        
        # Analytics: Entry frequency (days with entries)
        total_entries = user_entries.count()
        
        # Calendar logic: Only current month days
        import calendar
        cal = calendar.Calendar(firstweekday=6)
        # Get all days in the weeks that contain the month, then filter for current month
        all_days = [day for week in cal.monthdatescalendar(year, month) for day in week if day.month == month]
        
        # Map entries to dates for the calendar
        entries_by_date = {entry.date: entry for entry in user_entries}
        
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

class EntryCreateView(LoginRequiredMixin, CreateView):
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'journal/entry/entry_form.html'
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        date_str = request.GET.get('date')
        if date_str:
            try:
                date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                existing_entry = JournalEntry.objects.filter(user=request.user, date=date_obj).first()
                if existing_entry:
                    return redirect('entry_update', pk=existing_entry.pk)
            except ValueError:
                pass
        else:
            # Check for today if no date is specified
            today = timezone.now().date()
            existing_entry = JournalEntry.objects.filter(user=request.user, date=today).first()
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
        form.instance.user = self.request.user
        response = super().form_valid(form)
        images = self.request.FILES.getlist('images')
        for img in images:
            JournalImage.objects.create(entry=self.object, image=img)
        return response

class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'journal/entry/entry_form.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        images = self.request.FILES.getlist('images')
        if images:
            for img in images:
                JournalImage.objects.create(entry=self.object, image=img)
        return response

class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = JournalEntry
    success_url = reverse_lazy('dashboard')
    template_name = 'journal/entry/entry_confirm_delete.html'

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

class EntryDetailView(LoginRequiredMixin, DetailView):
    model = JournalEntry
    template_name = 'journal/entry/entry_detail.html'
    context_object_name = 'entry'

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

class TopicDetailView(LoginRequiredMixin, DetailView):
    model = Topic
    template_name = 'journal/topic/topic_detail.html'
    context_object_name = 'topic'

    def get_queryset(self):
        return Topic.objects.filter(user=self.request.user)

class TopicListView(LoginRequiredMixin, ListView):
    model = Topic
    template_name = 'journal/topic/topic_list.html'
    context_object_name = 'topics'

    def get_queryset(self):
        return Topic.objects.filter(user=self.request.user)

class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'journal/topic/topic_form.html'
    success_url = reverse_lazy('topic_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TopicUpdateView(LoginRequiredMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = 'journal/topic/topic_form.html'
    success_url = reverse_lazy('topic_list')

    def get_queryset(self):
        return Topic.objects.filter(user=self.request.user)

class TopicDeleteView(LoginRequiredMixin, DeleteView):
    model = Topic
    template_name = 'journal/topic/topic_confirm_delete.html'
    success_url = reverse_lazy('topic_list')

    def get_queryset(self):
        return Topic.objects.filter(user=self.request.user)

class EntryAutosaveView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            content_type = request.content_type.split(';')[0] if request.content_type else ''
            if content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            date_str = data.get('date')
            content = data.get('content')
            mood = data.get('mood')
            
            if not date_str or date_str == 'undefined':
                return JsonResponse({'status': 'error', 'message': 'Valid Date is required'}, status=400)
                
            try:
                date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({'status': 'error', 'message': f'Invalid date format: {date_str}'}, status=400)
            
            defaults = {}
            if content is not None: defaults['content'] = content
            if mood is not None: defaults['mood'] = mood
            
            if 'audio' in request.FILES:
                defaults['audio'] = request.FILES['audio']
            if 'video' in request.FILES:
                defaults['video'] = request.FILES['video']
                
            entry, created = JournalEntry.objects.update_or_create(
                user=request.user,
                date=date_obj,
                defaults=defaults
            )
            
            if 'images' in request.FILES:
                images = request.FILES.getlist('images')
                for img in images:
                    JournalImage.objects.create(entry=entry, image=img)
                    
            return JsonResponse({'status': 'success', 'id': entry.id})
        except Exception as e:
            print(f"Autosave error: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

class TopicAutosaveView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            topic_id = data.get('id')
            title = data.get('title')
            content = data.get('content')
            
            if topic_id:
                topic = Topic.objects.get(pk=topic_id, user=request.user)
                topic.title = title if title else topic.title
                topic.content = content if content is not None else topic.content
                topic.save()
            else:
                if title or content:
                    topic = Topic.objects.create(
                        user=request.user,
                        title=title if title else "Untitled Topic",
                        content=content if content else ""
                    )
                    topic_id = topic.id
                else:
                    return JsonResponse({'status': 'ignored'})
                    
            return JsonResponse({'status': 'success', 'id': topic_id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
