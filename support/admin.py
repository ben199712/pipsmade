from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import SupportCategory, SupportTicket, SupportMessage, SupportKnowledgeBase, SupportFAQ

@admin.register(SupportCategory)
class SupportCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_display', 'color_display', 'is_active', 'ticket_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']

    def icon_display(self, obj):
        return format_html('<i class="{}" style="color: var(--bs-{});"></i>', obj.icon, obj.color)
    icon_display.short_description = 'Icon'

    def color_display(self, obj):
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            obj.color,
            obj.color.title()
        )
    color_display.short_description = 'Color'

    def ticket_count(self, obj):
        count = obj.supportticket_set.count()
        return format_html('<span class="badge bg-info">{}</span>', count)
    ticket_count.short_description = 'Tickets'

class SupportMessageInline(admin.TabularInline):
    model = SupportMessage
    extra = 0
    readonly_fields = ['created_at', 'user']
    fields = ['user', 'message', 'is_staff_reply', 'attachment', 'created_at']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'subject', 'user_link', 'category', 'status', 'priority',
        'status_display', 'priority_display', 'assigned_to', 'created_at', 'last_activity'
    ]
    list_filter = [
        'status', 'priority', 'category', 'assigned_to',
        'created_at', 'resolved_at'
    ]
    search_fields = ['subject', 'description', 'user__username', 'user__email']
    list_editable = ['status', 'priority', 'assigned_to']
    readonly_fields = ['created_at', 'updated_at', 'resolved_at', 'closed_at', 'ip_address', 'user_agent']

    fieldsets = (
        ('Ticket Information', {
            'fields': ('user', 'category', 'subject', 'description')
        }),
        ('Status & Assignment', {
            'fields': ('status', 'priority', 'assigned_to')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'resolved_at', 'closed_at'),
            'classes': ('collapse',)
        }),
        ('Technical Information', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )

    inlines = [SupportMessageInline]

    actions = ['mark_resolved', 'mark_closed', 'assign_to_me']

    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'

    def status_display(self, obj):
        color = obj.get_status_color()
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status Display'

    def priority_display(self, obj):
        color = obj.get_priority_color()
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color,
            obj.get_priority_display()
        )
    priority_display.short_description = 'Priority Display'

    def last_activity(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return last_message.created_at
        return obj.created_at
    last_activity.short_description = 'Last Activity'

    def mark_resolved(self, request, queryset):
        updated = 0
        for ticket in queryset:
            if ticket.status != 'resolved':
                ticket.mark_resolved()
                updated += 1

        self.message_user(
            request,
            f'{updated} ticket(s) marked as resolved.'
        )
    mark_resolved.short_description = "Mark selected tickets as resolved"

    def mark_closed(self, request, queryset):
        updated = 0
        for ticket in queryset:
            if ticket.status != 'closed':
                ticket.mark_closed()
                updated += 1

        self.message_user(
            request,
            f'{updated} ticket(s) marked as closed.'
        )
    mark_closed.short_description = "Mark selected tickets as closed"

    def assign_to_me(self, request, queryset):
        updated = queryset.update(assigned_to=request.user)
        self.message_user(
            request,
            f'{updated} ticket(s) assigned to you.'
        )
    assign_to_me.short_description = "Assign selected tickets to me"

@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ['ticket_link', 'user', 'is_staff_reply', 'created_at', 'has_attachment']
    list_filter = ['is_staff_reply', 'created_at']
    search_fields = ['message', 'ticket__subject', 'user__username']
    readonly_fields = ['created_at', 'updated_at']

    def ticket_link(self, obj):
        url = reverse('admin:support_supportticket_change', args=[obj.ticket.id])
        return format_html('<a href="{}">#{} - {}</a>', url, obj.ticket.id, obj.ticket.subject)
    ticket_link.short_description = 'Ticket'

    def has_attachment(self, obj):
        return bool(obj.attachment)
    has_attachment.boolean = True
    has_attachment.short_description = 'Attachment'

# Customize admin site
admin.site.site_header = "pipsmade Admin"
admin.site.site_title = "pipsmade Admin Portal"
admin.site.index_title = "Welcome to pipsmade Administration"
