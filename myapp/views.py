from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Room, TenantProfile, Payment, MaintenanceRequest, Announcement
from .forms import SignUpForm, PaymentForm, MaintenanceForm, AnnouncementForm
from django.contrib.auth.models import User
from django.contrib import messages

def index(request):
    context = {
        "hostel": {
            "name": "Grace Apartments",
            "description": "Affordable bedsitters and single rooms for students...",
            "image_url": "/static/assets/hostel.jpg",  # or blank
            "about": "Located close to campus and public transport...",
            "room_types": "Bedsitters and singles",
            "payment_info": "Paybill (show confirmation or submit online)",
            "maintenance_info": "Report to caretaker or via portal",
        },
        "caretaker": {
            "name": "Joseph",
            "phone": "0712 345 678"
        }
    }
    return render(request, 'index.html', context)

def rooms_list(request):
    rooms = Room.objects.all()
    return render(request, 'rooms_details.html', {'rooms': rooms})

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Redirect based on user type
            if user.user_type == 'admin':
                return redirect('admin_dashboard')
            else:  # tenant
                return redirect('tenant_dashboard')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'admin':
            return redirect('admin_dashboard')
        return redirect('tenant_dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect based on user type
            if user.user_type == 'admin':
                return redirect('admin_dashboard')
            return redirect('tenant_dashboard')
            
        return render(request, 'login.html', {'error': 'Invalid username or password'})
        
    return render(request, 'login.html')

def payments_view(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Later you'll save it to DB, for now we pretend
            print("Payment saved:", form.cleaned_data)
            return redirect('tenant_dashboard')
    else:
        form = PaymentForm()

    return render(request, 'payments.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def tenant_dashboard(request):
    try:
        profile = request.user.tenantprofile
    except TenantProfile.DoesNotExist:
        # redirect to signup or show message
        return redirect('sign_up')

    payments = Payment.objects.filter(tenant=profile).order_by('-id')
    issues = MaintenanceRequest.objects.filter(tenant=profile).order_by('-id')
    announcements = Announcement.objects.order_by('-id')[:5]
    return render(request, 'tenant_dashboard.html', {
        'profile': profile, 'payments': payments, 'issues': issues, 'announcements': announcements
    })

@login_required
def submit_payment(request):
    profile = request.user.tenantprofile
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save(commit=False)
            p.tenant = profile
            p.status = 'pending'
            p.save()
            return redirect('tenant_dashboard')
    else:
        form = PaymentForm()
    return render(request, 'payments.html', {'form': form})

@login_required
def tenant_payments(request):
    payments = Payment.objects.filter(tenant=request.user.tenantprofile).order_by('-id')
    return render(request, 'payments.html', {'payments': payments})


@login_required
def submit_maintenance(request):
    print("\n=== DEBUG: Starting submit_maintenance view ===")
    print(f"User: {request.user}")
    print(f"Method: {request.method}")
    
    if not hasattr(request.user, 'tenantprofile'):
        print("ERROR: User has no tenantprofile")
        return redirect('admin_dashboard')  # Add appropriate error handling

    profile = request.user.tenantprofile
    print(f"Tenant Profile: {profile.id} - {profile.user.get_full_name()}")
    
    if request.method == 'POST':
        print("Form data:", request.POST)  # Debug form data
        form = MaintenanceForm(request.POST, request.FILES)
        print("Form is valid:", form.is_valid())
        print("Form errors:", form.errors if not form.is_valid() else "No errors")
        
        if form.is_valid():
            try:
                m = form.save(commit=False)
                m.tenant = profile
                m.status = 'pending'
                print("Saving maintenance request with data:", {
                    'category': m.category,
                    'description': m.description,
                    'status': m.status,
                    'tenant': m.tenant.id
                })
                m.save()
                print("Maintenance request saved successfully!")
                messages.success(request, 'Your maintenance request has been submitted.')
                return redirect('tenant_dashboard')
            except Exception as e:
                print("ERROR saving maintenance request:", str(e))
                messages.error(request, f'Error submitting maintenance request: {str(e)}')
        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = MaintenanceForm()
    
    return render(request, 'maintenance.html', {'form': form})

# Admin views (staff only)
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_dashboard(request):
    total_rooms = Room.objects.count()
    occupied = Room.objects.filter(status__iexact='occupied').count()
    vacant = Room.objects.filter(status__iexact='vacant').count()
    maintenance_pending = MaintenanceRequest.objects.filter(status__iexact='pending').count()
    tenants = TenantProfile.objects.all()
    #payments_pending = Payment.objects.filter(status='pending').count()
    return render(request, 'admin_dashboard.html', {
        'total_rooms': total_rooms, 'occupied': occupied, 'vacant': vacant,
        'maintenance_pending': maintenance_pending, 'tenants': tenants, #'payments_pending': payments_pending
    })

@staff_member_required
def admin_maintenance_list(request):
    # Get filter parameter if it exists
    status_filter = request.GET.get('status', 'all')
    
    # Query all maintenance requests
    issues = MaintenanceRequest.objects.all().order_by('-id')
    
    # Apply status filter if not 'all'
    if status_filter != 'all':
        issues = issues.filter(status=status_filter)
    
    # Get counts for each status
    all_count = MaintenanceRequest.objects.count()
    pending_count = MaintenanceRequest.objects.filter(status='pending').count()
    in_progress_count = MaintenanceRequest.objects.filter(status='in_progress').count()
    completed_count = MaintenanceRequest.objects.filter(status='completed').count()
    
    return render(request, 'admin_maintenance.html', {
        'issues': issues,
        'status_filter': status_filter,
        'all_count': all_count,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
    })

@staff_member_required
def approve_payment(request, payment_id):
    p = get_object_or_404(Payment, id=payment_id)
    p.status = 'approved'
    p.save()
    return redirect('admin_dashboard')

@staff_member_required
def admin_rooms(request):
    rooms = Room.objects.all().order_by('room_number')
    return render(request, 'admin_rooms.html', {'rooms': rooms})

@staff_member_required
def admin_tenants(request):
    tenants = TenantProfile.objects.select_related('user', 'room').all()
    return render(request, 'admin_tenants.html', {'tenants': tenants})

@staff_member_required
def admin_announcements(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Announcement created successfully!')
            return redirect('admin_announcements')
    else:
        form = AnnouncementForm()
    
    announcements = Announcement.objects.all().order_by('-id')
    return render(request, 'admin_announcements.html', {
        'form': form,
        'announcements': announcements
    })