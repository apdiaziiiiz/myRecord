from django.contrib import admin
from .models import JournalEntry, JournalImage

class JournalImageInline(admin.TabularInline):
    model = JournalImage
    extra = 1

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('date', 'mood', 'created_at')
    list_filter = ('mood', 'date')
    search_fields = ('content',)
    inlines = [JournalImageInline]
