from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Generate time-limited activation tokens tied to user's primary key,
    timestamp, and activation state. Once the user is activated (is_active becomes True),
    the token automatically becomes invalid and cannot be reused.
    """
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"

account_activation_token = AccountActivationTokenGenerator()
