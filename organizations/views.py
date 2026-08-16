from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse
from .models import Organization, Feedback
from .forms import OrganizationForm, FeedbackForm
from django.urls import reverse
from io import BytesIO
import qrcode

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    organizations = request.user.organizations.all()
    return render(request, 'organizations/dashboard.html', {'organizations': organizations})

@login_required
def add_organization(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            org = form.save(commit=False)
            org.user = request.user
            # build site_url if needed dynamically, though settings is used in save()
            # To ensure it uses the correct host dynamically we can pass it, 
            # but model save() does not have request. So we can update it before saving
            # Actually, doing it in the model is fine for local.
            # But let's build absolute URI and save it as a custom attribute just in case.
            org.save()
            return redirect('org_detail', org_id=org.id)
    else:
        form = OrganizationForm()
    return render(request, 'organizations/add_organization.html', {'form': form})

@login_required
def organization_detail(request, org_id):
    org = get_object_or_404(Organization, id=org_id, user=request.user)
    feedbacks = org.feedbacks.all().order_by('-created_at')
    
    # Absolute URL for display
    feedback_link = request.build_absolute_uri(reverse('submit_feedback', args=[org.id]))
    
    return render(request, 'organizations/org_detail.html', {
        'org': org,
        'feedbacks': feedbacks,
        'feedback_link': feedback_link
    })

def organization_qr(request, org_id):
    """Tashkilotning QR kodini har safar so'rov kelganda PNG qilib generatsiya qiladi.

    Diskda saqlamaymiz: shunda QR ichidagi havola doim joriy domenga mos keladi
    va deploy paytida fayllar yo'qolib qolsa ham rasm buzilmaydi.
    """
    org = get_object_or_404(Organization, id=org_id)
    feedback_url = request.build_absolute_uri(reverse('submit_feedback', args=[org.id]))

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(feedback_url)
    qr.make(fit=True)

    buffer = BytesIO()
    qr.make_image(fill_color="black", back_color="white").save(buffer, format="PNG")

    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    if 'download' in request.GET:
        filename = f"qr_{org.id}.png"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@login_required
def edit_organization(request, org_id):
    org = get_object_or_404(Organization, id=org_id, user=request.user)
    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=org)
        if form.is_valid():
            form.save()
            return redirect('org_detail', org_id=org.id)
    else:
        form = OrganizationForm(instance=org)
    return render(request, 'organizations/edit_organization.html', {'form': form, 'org': org})

@login_required
def delete_organization(request, org_id):
    org = get_object_or_404(Organization, id=org_id, user=request.user)
    if request.method == 'POST':
        if org.qr_code:
            # eski yozuvlarda qolgan QR fayli bo'lsa, u ham tozalansin
            org.qr_code.delete(save=False)
        org.delete()
        return redirect('dashboard')
    return render(request, 'organizations/delete_organization.html', {'org': org})

def submit_feedback(request, org_id):
    org = get_object_or_404(Organization, id=org_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.organization = org
            feedback.save()
            return redirect('feedback_success')
    else:
        form = FeedbackForm()
    return render(request, 'organizations/submit_feedback.html', {'form': form, 'org': org})

def feedback_success(request):
    return render(request, 'organizations/feedback_success.html')
