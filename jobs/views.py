from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import MovingRequestForm
from .models import MovingRequest, JobAssignment
from profiles.models import Profile
from django.contrib import messages

# Create your views here.
@login_required
def create_request_view(request):
    if request.user.profile.role != "customer":
        return redirect("dashboard")

    if request.method == "POST":
        form = MovingRequestForm(request.POST)
        if form.is_valid():
            moving_request = form.save(commit=False)
            moving_request.customer = request.user
            moving_request.status = 'pending'
            moving_request.save()
            return redirect("dashboard")
    else:
        form = MovingRequestForm()

    return render(request, "jobs/create_request.html", {"form": form})

@login_required
def request_list(request):
    """
    Show all moving requests created by the logged-in customer.
    """
    requests = MovingRequest.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'jobs/request_list.html', {'requests': requests})

@login_required
def request_detail(request, request_id):
    """
    Show a single request with details.
    """
    moving_request = get_object_or_404(MovingRequest, id=request_id, customer=request.user)
    #TODO: further filter movers based on service area
    available_movers = Profile.objects.filter(role='mover', service_area__icontains=moving_request.pickup_location)
    return render(request, 'jobs/request_detail.html', {
        'request_obj': moving_request,
        'movers': available_movers
    })

@login_required
def available_jobs(request):
    if request.user.profile.role != 'mover':
        return redirect('dashboard')  # or raise 403

    jobs = JobAssignment.objects.filter(
        mover = request.user,
        status='assigned'
    ).order_by('assigned_at')

    return render(request, 'jobs/available_jobs.html', {'jobs': jobs})


@login_required
def accept_job(request, request_id):
    """
    Accept a moving job and create a JobAssignment.
    """
    if request.user.profile.role != 'mover':
        return redirect('dashboard')  # or raise 403

    job_assignment = get_object_or_404(
        JobAssignment,
        moving_request__id=request_id,
        mover=request.user
    )

    if job_assignment.status == 'assigned':
        job_assignment.status = 'in_progress'
        job_assignment.save()

    return redirect('my_jobs')


@login_required
def my_jobs(request):
    """
    View assigned and completed jobs for the mover.
    """
    if request.user.profile.role != 'mover':
        return redirect('dashboard')  # or raise 403

    jobs = JobAssignment.objects.filter(
        mover=request.user
    ).order_by('-assigned_at')

    return render(request, 'jobs/my_jobs.html', {'jobs': jobs})

@login_required
def accept_mover(request, request_id):
    """
    Customer accepts a mover for their moving request.
    Expects a POST with 'mover_id' (the User id of the mover to assign).
    """
    moving_request = get_object_or_404(MovingRequest, id=request_id, customer=request.user)

    if request.method == 'POST':
        mover_id = request.POST.get('mover_id')
        if not mover_id:
            messages.error(request, "No mover selected.")
            return redirect('request_detail', request_id=request_id)

        from django.contrib.auth.models import User
        mover = get_object_or_404(User, id=mover_id)

        # Prevent double-assignment
        if JobAssignment.objects.filter(moving_request=moving_request).exists():
            messages.warning(request, "This request already has a mover assigned.")
            return redirect('request_detail', request_id=request_id)

        # Create JobAssignment
        JobAssignment.objects.create(
            moving_request=moving_request,
            mover=mover,
            status='assigned',
            agreed_price=moving_request.budget
        )

        # Update request status
        moving_request.status = 'accepted'
        moving_request.save()

        messages.success(request, f"{mover.username} has been assigned to your moving request.")
        return redirect('request_detail', request_id=request_id)

    # If GET, redirect to request detail
    return redirect('request_detail', request_id=request_id)