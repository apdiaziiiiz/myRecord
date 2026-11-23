from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import authenticate, password_validation
from .models import JournalEntry, JournalImage, Topic

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class JournalEntryForm(forms.ModelForm):
    images = MultipleFileField(required=False, label="Photos")

    class Meta:
        model = JournalEntry
        fields = ['date', 'mood', 'content', 'audio', 'video']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your thoughts here...'}),
            'mood': forms.Select(attrs={'class': 'mood-select'}),
        }

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Topic Title...'}),
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your thoughts here...'}),
        }

class CustomUserCreationForm(forms.ModelForm):
    """
    Registration form collecting unique username, unique email,
    and password confirmation with full Django password validation.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'real-input'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'class': 'real-input', 'id': 'passwordInput'})
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'class': 'real-input', 'id': 'confirmPasswordInput'})
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'real-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', "Passwords do not match.")
            else:
                temp_user = User(
                    username=cleaned_data.get('username', ''),
                    email=cleaned_data.get('email', '')
                )
                try:
                    password_validation.validate_password(password, temp_user)
                except forms.ValidationError as error:
                    self.add_error('password', error)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        user.is_active = False  # Account stays inactive until email is verified
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    """
    Authentication form that cleanly differentiates between wrong credentials
    and unverified (inactive) accounts with actionable user guidance.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'real-input'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'class': 'real-input', 'id': 'passwordInput'})
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                # Check if credentials match an inactive account
                try:
                    user_match = User.objects.get(username__iexact=username)
                    if user_match.check_password(password) and not user_match.is_active:
                        raise forms.ValidationError(
                            "This account is not verified yet. Please check your email, or request a new verification link below.",
                            code='inactive',
                        )
                except User.DoesNotExist:
                    pass

                raise forms.ValidationError(
                    "Invalid username or password.",
                    code='invalid_login',
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

class ResendVerificationForm(forms.Form):
    """
    Form to request a new activation email link.
    """
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your registered email', 'class': 'real-input'})
    )

class CustomPasswordResetForm(PasswordResetForm):
    """
    Styled password reset request form.
    """
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your registered email', 'class': 'real-input'})
    )

class CustomSetPasswordForm(SetPasswordForm):
    """
    Styled form for setting a new password during reset confirmation.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'real-input', 'placeholder': '••••••••'})
