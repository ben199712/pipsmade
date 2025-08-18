from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import SupportTicket, SupportMessage, SupportCategory, SupportKnowledgeBase, SupportFAQ
from .forms import SupportTicketForm, SupportMessageForm, QuickSupportForm, AdminTicketUpdateForm, EmailSupportForm
from .email_notifications import send_support_notification

@login_required
def support_center(request):
    """Main support center page"""
    # Get user's tickets for statistics (don't slice here)
    user_tickets_all = SupportTicket.objects.filter(user=request.user)
    
    # Get user's recent tickets (slice after getting the base queryset)
    user_tickets = user_tickets_all[:5]

    # Get featured knowledge base articles
    featured_articles = SupportKnowledgeBase.objects.filter(
        is_published=True,
        is_featured=True
    )[:6]

    # Get popular FAQs
    popular_faqs = SupportFAQ.objects.filter(is_active=True)[:8]

    # Get support categories
    categories = SupportCategory.objects.filter(is_active=True)

    # Get user notifications
    from transactions.models import TransactionNotification
    unread_notifications = TransactionNotification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by('-created_at')[:10]

    # Support statistics (use the unsliced queryset)
    stats = {
        'total_tickets': user_tickets_all.count(),
        'open_tickets': user_tickets_all.filter(status='open').count(),
        'resolved_tickets': user_tickets_all.filter(status='resolved').count(),
    }

    context = {
        'user_tickets': user_tickets,
        'featured_articles': featured_articles,
        'popular_faqs': popular_faqs,
        'categories': categories,
        'stats': stats,
        'unread_notifications': unread_notifications,
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

@login_required
def email_support(request):
    """Handle email support requests"""
    print(f"Email support view called with method: {request.method}")
    
    if request.method == 'POST':
        print("Processing POST request")
        print(f"POST data: {request.POST}")
        print(f"FILES data: {request.FILES}")
        
        form = EmailSupportForm(request.POST, request.FILES)
        print(f"Form is valid: {form.is_valid()}")
        
        if form.is_valid():
            print("Form is valid, processing...")
            try:
                # Get form data
                topic = form.cleaned_data['topic']
                priority = form.cleaned_data['priority']
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                contact_email = form.cleaned_data['contact_email']
                attachments = request.FILES.getlist('attachments')
                
                print(f"Form data - Topic: {topic}, Priority: {priority}, Subject: {subject}")
                print(f"Contact email: {contact_email}, Attachments count: {len(attachments)}")
                
                # Create support ticket
                category, _ = SupportCategory.objects.get_or_create(
                    name=topic.title(),
                    defaults={
                        'description': f'Email support for {topic}',
                        'icon': 'fas fa-envelope',
                        'color': 'primary'
                    }
                )
                
                print(f"Category: {category.name}")
                
                # Create ticket
                ticket = SupportTicket.objects.create(
                    user=request.user,
                    category=category,
                    priority=priority,
                    subject=subject,
                    message=message,
                    status='open'
                )
                
                print(f"Ticket created with ID: {ticket.id}")
                
                # Handle attachments
                if attachments:
                    for attachment in attachments:
                        support_message = SupportMessage.objects.create(
                            ticket=ticket,
                            user=request.user,
                            message=f"Email support request from {contact_email}",
                            is_staff_reply=False
                        )
                        support_message.attachment = attachment
                        support_message.save()
                        print(f"Attachment saved: {attachment.name}")
                
                # Send admin notification email using the simple email system
                try:
                    send_support_notification(ticket)
                    print("Admin notification sent successfully via simple email system")
                except Exception as e:
                    # Log email error but don't fail the request
                    print(f"Failed to send admin notification via simple email system: {e}")
                    
                    # Fallback to old method
                    try:
                        admin_subject = f"New Email Support Request - #{ticket.id}"
                        admin_message = f"""
                        New email support request received:

                        Ticket ID: #{ticket.id}
                        User: {request.user.get_full_name() or request.user.username} ({request.user.email})
                        Contact Email: {contact_email}
                        Topic: {topic.title()}
                        Priority: {priority.title()}
                        Subject: {subject}
                        Message: {message}

                        View ticket: {request.build_absolute_uri(f'/admin/support/supportticket/{ticket.id}/')}
                        """
                        
                        send_mail(
                            subject=admin_subject,
                            message=strip_tags(admin_message),
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[settings.ADMIN_EMAIL],
                            fail_silently=True,
                        )
                        print("Admin notification sent successfully via fallback method")
                    except Exception as e2:
                        print(f"Failed to send admin notification via fallback method: {e2}")
                
                messages.success(
                    request, 
                    f'Your email support request has been sent successfully! Ticket #{ticket.id} has been created. We will respond within 2-4 hours.'
                )
                
                print("Returning success response")
                return JsonResponse({
                    'success': True,
                    'message': f'Email sent successfully! Ticket #{ticket.id} created.',
                    'ticket_id': ticket.id
                })
                
            except Exception as e:
                print(f"Error in email support: {str(e)}")
                return JsonResponse({
                    'success': False,
                    'message': 'An error occurred while processing your request. Please try again.'
                }, status=500)
        else:
            print(f"Form errors: {form.errors}")
            return JsonResponse({
                'success': False,
                'message': 'Please correct the errors in your form.',
                'errors': form.errors
            }, status=400)
    
    return render(request, 'support/email_support.html')

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
