from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.views import View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
from django.conf import settings
from django.db.models import Count
from django.utils import timezone
from .models import JournalEntry, JournalImage, Topic
from .forms import (
    JournalEntryForm,
    TopicForm,
    CustomUserCreationForm,
    ResendVerificationForm,
)
from .tokens import account_activation_token
import datetime
import calendar
import json


def send_verification_email(request, user):
    """
    Sends a time-limited account activation link with HTML and plain text alternatives.
    """
    token = account_activation_token.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    activation_url = request.build_absolute_uri(
        reverse('activate', kwargs={'uidb64': uidb64, 'token': token})
    )
    context = {
        'user': user,
        'activation_url': activation_url,
        'protocol': 'https' if request.is_secure() else 'http',
        'domain': request.get_host(),
        'uid': uidb64,
        'token': token,
    }
    subject = "Verify your MyJournal email address"
    text_content = render_to_string('journal/emails/activation_email.txt', context)
    html_content = render_to_string('journal/emails/activation_email.html', context)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                send_verification_email(request, user)
            except Exception as e:
                print(f"Error sending activation email: {e}")
            request.session['verification_email'] = user.email
            return redirect('verification_sent')
    else:
        form = CustomUserCreationForm()
    return render(request, 'journal/auth/signup.html', {'form': form})


def verification_sent_view(request):
    email = request.session.get('verification_email', '')
    return render(request, 'journal/auth/verification_sent.html', {'email': email})


def activate_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'journal/auth/activation_success.html', {'user': user})
    else:
        return render(request, 'journal/auth/activation_invalid.html')


def resend_verification_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = ResendVerificationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip().lower()
            user = User.objects.filter(email__iexact=email, is_active=False).first()
            if user:
                try:
                    send_verification_email(request, user)
                except Exception as e:
                    print(f"Error resending verification email: {e}")
            # Prevents email enumeration by always showing success page
            request.session['verification_email'] = email
            return redirect('verification_sent')
    else:
        initial_email = request.GET.get('email', '')
        form = ResendVerificationForm(initial={'email': initial_email})

    return render(request, 'journal/auth/resend_verification.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


@login_required
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        for entry in user.entries.all():
            for img in entry.images.all():
                if img.image:
                    try:
                        img.image.delete(save=False)
                    except Exception:
                        pass
            if entry.audio:
                try:
                    entry.audio.delete(save=False)
                except Exception:
                    pass
            if entry.video:
                try:
                    entry.video.delete(save=False)
                except Exception:
                    pass
        logout(request)
        user.delete()
        return redirect('login')
    return redirect('dashboard')


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
        
        # Calendar logic: All days of current month
        cal = calendar.Calendar(firstweekday=6)
        all_days = [day for week in cal.monthdatescalendar(year, month) for day in week if day.month == month]
        
        # Map entries to dates for the calendar
        entries_by_date = {entry.date: entry for entry in user_entries}
        
        # Check if user has written an entry for today
        today_entry = entries_by_date.get(today)
        
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
            'today_entry': today_entry,
            'view_date': datetime.date(year, month, 1),
        })
        return context

class EntryCreateView(LoginRequiredMixin, CreateView):
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'journal/entry/entry_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
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

    def get_success_url(self):
        return reverse_lazy('entry_detail', kwargs={'pk': self.object.pk})

class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'journal/entry/entry_form.html'

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        images = self.request.FILES.getlist('images')
        if images:
            for img in images:
                JournalImage.objects.create(entry=self.object, image=img)
        return response

    def get_success_url(self):
        return reverse_lazy('entry_detail', kwargs={'pk': self.object.pk})

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

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('topic_detail', kwargs={'pk': self.object.pk})

class TopicUpdateView(LoginRequiredMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = 'journal/topic/topic_form.html'

    def get_queryset(self):
        return Topic.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('topic_detail', kwargs={'pk': self.object.pk})

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
