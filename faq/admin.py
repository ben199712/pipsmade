from django.contrib import admin
from .models import FAQCategory, FAQ

@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active', 'faq_count', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']
    prepopulated_fields = {'slug': ('name',)}
    
    def faq_count(self, obj):
        return obj.faqs.count()
    faq_count.short_description = 'FAQ Count'

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_active', 'is_featured', 'created_at']
    list_editable = ['order', 'is_active', 'is_featured']
    list_filter = ['category', 'is_active', 'is_featured', 'created_at']
    search_fields = ['question', 'answer']
    ordering = ['-is_featured', 'order', 'question']
    list_per_page = 25
    change_list_template = 'admin/faq/faq/change_list.html'
    
    fieldsets = (
        ('Question & Answer', {
            'fields': ('question', 'answer')
        }),
        ('Organization', {
            'fields': ('category', 'order', 'is_featured')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
