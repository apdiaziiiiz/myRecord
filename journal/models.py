from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class JournalEntry(models.Model):
    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('neutral', 'Neutral'),
        ('productive', 'Productive'),
        ('tired', 'Tired'),
        ('excited', 'Excited'),
        ('angry', 'Angry'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=6)
    content = models.TextField()
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, default='neutral')
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Media fields (Optional)
    audio = models.FileField(upload_to='audio/%Y/%m/%d/', blank=True, null=True)
    video = models.FileField(upload_to='video/%Y/%m/%d/', blank=True, null=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name_plural = "Journal Entries"
        constraints = [
            models.UniqueConstraint(fields=['user', 'date'], name='unique_user_date')
        ]

    def __str__(self):
        return f"{self.date} - {self.get_mood_display()}"

class JournalImage(models.Model):
    entry = models.ForeignKey(JournalEntry, related_name='images', on_delete=models.CASCADE)
    image = models.FileField(upload_to='images/%Y/%m/%d/')

    def __str__(self):
        return f"Image for {self.entry.date}"

class Topic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=6)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
