from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views, forms

urlpatterns = [
    # Authentication & Email Verification URLs
    path('', auth_views.LoginView.as_view(
        template_name='journal/auth/login.html',
        authentication_form=forms.CustomAuthenticationForm,
        redirect_authenticated_user=True,
    ), name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('verification-sent/', views.verification_sent_view, name='verification_sent'),
    path('activate/<uidb64>/<token>/', views.activate_view, name='activate'),
    path('resend-verification/', views.resend_verification_view, name='resend_verification'),
    path('logout/', views.logout_view, name='logout'),
    path('delete-account/', views.delete_account_view, name='delete_account'),

    # Password Reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='journal/auth/password_reset_form.html',
        email_template_name='journal/emails/password_reset_email.txt',
        html_email_template_name='journal/emails/password_reset_email.html',
        subject_template_name='journal/emails/password_reset_subject.txt',
        form_class=forms.CustomPasswordResetForm,
        success_url=reverse_lazy('password_reset_done'),
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='journal/auth/password_reset_done.html',
    ), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='journal/auth/password_reset_confirm.html',
        form_class=forms.CustomSetPasswordForm,
        success_url=reverse_lazy('password_reset_complete'),
    ), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='journal/auth/password_reset_complete.html',
    ), name='password_reset_complete'),

    # Dashboard & Journal URLs
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('entry/new/', views.EntryCreateView.as_view(), name='entry_create'),
    path('entry/<int:pk>/', views.EntryDetailView.as_view(), name='entry_detail'),
    path('entry/<int:pk>/edit/', views.EntryUpdateView.as_view(), name='entry_update'),
    path('entry/<int:pk>/delete/', views.EntryDeleteView.as_view(), name='entry_delete'),

    # Topic URLs
    path('topics/', views.TopicListView.as_view(), name='topic_list'),
    path('topics/new/', views.TopicCreateView.as_view(), name='topic_create'),
    path('topics/<int:pk>/edit/', views.TopicUpdateView.as_view(), name='topic_update'),
    path('topics/<int:pk>/delete/', views.TopicDeleteView.as_view(), name='topic_delete'),
    path('topics/<int:pk>/', views.TopicDetailView.as_view(), name='topic_detail'),

    # Autosave endpoints
    path('entry/autosave/', views.EntryAutosaveView.as_view(), name='entry_autosave'),
    path('topics/autosave/', views.TopicAutosaveView.as_view(), name='topic_autosave'),
]
