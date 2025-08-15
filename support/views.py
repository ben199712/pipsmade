from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import SupportTicket, SupportMessage, SupportCategory, SupportKnowledgeBase, SupportFAQ
from .forms import SupportTicketForm, SupportMessageForm, QuickSupportForm, AdminTicketUpdateForm

@login_required
def support_center(request):
    """Main support center page"""
    # Get user's recent tickets
    user_tickets = SupportTicket.objects.filter(user=request.user)[:5]

    # Get featured knowledge base articles
    featured_articles = SupportKnowledgeBase.objects.filter(
        is_published=True,
        is_featured=True
    )[:6]

    # Get popular FAQs
    popular_faqs = SupportFAQ.objects.filter(is_active=True)[:8]

    # Get support categories
    categories = SupportCategory.objects.filter(is_active=True)

    # Support statistics
    stats = {
        'total_tickets': user_tickets.count(),
        'open_tickets': user_tickets.filter(status='open').count(),
        'resolved_tickets': user_tickets.filter(status='resolved').count(),
    }

    context = {
        'user_tickets': user_tickets,
        'featured_articles': featured_articles,
        'popular_faqs': popular_faqs,
        'categories': categories,
        'stats': stats,
    }

    return render(request, 'dashboard/support.html', context)

@login_required
def create_ticket(request):
    """Create a new support ticket"""
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.ip_address = request.META.get('REMOTE_ADDR')
            ticket.user_agent = request.META.get('HTTP_USER_AGENT', '')
            ticket.save()

            messages.success(request, f'Support ticket #{ticket.id} created successfully!')
            return redirect('support:ticket_detail', ticket_id=ticket.id)
    else:
        form = SupportTicketForm()

    context = {
        'form': form,
        'categories': SupportCategory.objects.filter(is_active=True),
    }

    return render(request, 'support/create_ticket.html', context)

@login_required
def ticket_detail(request, ticket_id):
    """View and respond to a support ticket"""
    ticket = get_object_or_404(SupportTicket, id=ticket_id, user=request.user)

    if request.method == 'POST':
        form = SupportMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.ticket = ticket
            message.user = request.user
            message.is_staff_reply = False
            message.save()

            # Update ticket status if it was resolved/closed
            if ticket.status in ['resolved', 'closed']:
                ticket.status = 'open'
                ticket.save()

            messages.success(request, 'Your message has been added to the ticket.')
            return redirect('support:ticket_detail', ticket_id=ticket.id)
    else:
        form = SupportMessageForm()

    # Get all messages for this ticket
    messages_list = ticket.messages.all()

    context = {
        'ticket': ticket,
        'messages': messages_list,
        'form': form,
    }

    return render(request, 'support/ticket_detail.html', context)

@login_required
def my_tickets(request):
    """List user's support tickets"""
    tickets = SupportTicket.objects.filter(user=request.user)

    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        tickets = tickets.filter(status=status_filter)

    # Search
    search_query = request.GET.get('search')
    if search_query:
        tickets = tickets.filter(
            Q(subject__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(tickets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
    }

    return render(request, 'support/my_tickets.html', context)

@login_required
def knowledge_base(request):
    """Knowledge base articles"""
    articles = SupportKnowledgeBase.objects.filter(is_published=True)

    # Filter by category if provided
    category_id = request.GET.get('category')
    if category_id:
        articles = articles.filter(category_id=category_id)

    # Search
    search_query = request.GET.get('search')
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(keywords__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(articles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = SupportCategory.objects.filter(is_active=True)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
    }

    return render(request, 'support/knowledge_base.html', context)

@login_required
def article_detail(request, slug):
    """View knowledge base article"""
    article = get_object_or_404(SupportKnowledgeBase, slug=slug, is_published=True)

    # Increment view count
    article.view_count += 1
    article.save(update_fields=['view_count'])

    # Get related articles
    related_articles = SupportKnowledgeBase.objects.filter(
        category=article.category,
        is_published=True
    ).exclude(id=article.id)[:5]

    context = {
        'article': article,
        'related_articles': related_articles,
    }

    return render(request, 'support/article_detail.html', context)

@login_required
def faq_list(request):
    """FAQ list page"""
    faqs = SupportFAQ.objects.filter(is_active=True)

    # Filter by category if provided
    category_id = request.GET.get('category')
    if category_id:
        faqs = faqs.filter(category_id=category_id)

    # Search
    search_query = request.GET.get('search')
    if search_query:
        faqs = faqs.filter(
            Q(question__icontains=search_query) |
            Q(answer__icontains=search_query)
        )

    categories = SupportCategory.objects.filter(is_active=True)

    context = {
        'faqs': faqs,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
    }

    return render(request, 'support/faq_list.html', context)

@login_required
def search_support(request):
    """Search support content"""
    query = request.GET.get('q', '')
    results = []

    if query:
        # Search knowledge base
        kb_results = SupportKnowledgeBase.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(keywords__icontains=query),
            is_published=True
        )[:10]

        # Search FAQs
        faq_results = SupportFAQ.objects.filter(
            Q(question__icontains=query) |
            Q(answer__icontains=query),
            is_active=True
        )[:10]

        results = {
            'articles': kb_results,
            'faqs': faq_results,
            'query': query,
        }

    return render(request, 'support/search_results.html', results)

@login_required
def quick_help(request):
    """Quick help page with common solutions"""
    if request.method == 'POST':
        form = QuickSupportForm(request.POST)
        if form.is_valid():
            # Create a quick support ticket
            issue_type = form.cleaned_data['issue_type']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Find or create category
            category, _ = SupportCategory.objects.get_or_create(
                name='Quick Help',
                defaults={
                    'description': 'Quick help requests',
                    'icon': 'fas fa-bolt',
                    'color': 'warning'
                }
            )

            # Create ticket
            ticket = SupportTicket.objects.create(
                user=request.user,
                category=category,
                subject=f"Quick Help: {dict(form.ISSUE_TYPES)[issue_type]}",
                description=message,
                priority='medium',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

            messages.success(request, f'Quick help ticket #{ticket.id} created successfully!')
            return redirect('support:ticket_detail', ticket_id=ticket.id)
    else:
        form = QuickSupportForm()

    # Get common FAQs
    common_faqs = SupportFAQ.objects.filter(is_active=True)[:6]

    context = {
        'form': form,
        'common_faqs': common_faqs,
    }

    return render(request, 'support/quick_help.html', context)

# AJAX Views
@login_required
def ajax_search(request):
    """AJAX search for support content"""
    query = request.GET.get('q', '')
    results = []

    if query and len(query) >= 3:
        # Search knowledge base
        articles = SupportKnowledgeBase.objects.filter(
            Q(title__icontains=query) |
            Q(keywords__icontains=query),
            is_published=True
        )[:5]

        # Search FAQs
        faqs = SupportFAQ.objects.filter(
            Q(question__icontains=query),
            is_active=True
        )[:5]

        results = {
            'articles': [
                {
                    'title': article.title,
                    'url': f'/support/kb/{article.slug}/',
                    'type': 'article'
                }
                for article in articles
            ],
            'faqs': [
                {
                    'question': faq.question,
                    'answer': faq.answer[:200] + '...' if len(faq.answer) > 200 else faq.answer,
                    'type': 'faq'
                }
                for faq in faqs
            ]
        }

    return JsonResponse(results)

@login_required
def ajax_close_ticket(request, ticket_id):
    """AJAX close ticket"""
    if request.method == 'POST':
        ticket = get_object_or_404(SupportTicket, id=ticket_id, user=request.user)

        if ticket.status not in ['resolved', 'closed']:
            ticket.mark_closed()
            return JsonResponse({
                'success': True,
                'message': 'Ticket closed successfully',
                'status': ticket.get_status_display()
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Ticket is already closed'
            })

    return JsonResponse({'success': False, 'message': 'Invalid request'})
