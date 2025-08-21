from django.contrib import admin
import datetime
# Register your models here.
from entries.models import LogEntries

@admin.register(LogEntries)
class LogEntriesAdmin(admin.ModelAdmin):
    list_display = ('user', 'formatted_entered', 'formatted_exited','visit_duration')

    def formatted_entered(self, obj):
        return obj.entered_at.strftime("%d-%m-%Y %I:%M %p")
    formatted_entered.short_description = 'Entered At'

    def formatted_exited(self, obj):
        return obj.exited_at.strftime("%d-%m-%Y %I:%M %p") if obj.exited_at else "Still inside"
    formatted_exited.short_description = 'Exited At'

    def visit_duration(self, obj):
        duration = obj.duration()
        if duration:
            # Format as hours and minutes
            total_seconds = int(duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{hours}h {minutes}m"
        return "Still inside"
    visit_duration.short_description = 'Duration'
