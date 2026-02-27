from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import MovingRequestForm, BidForm
from .models import MovingRequest, Bid
from profiles.models import MoverProfile, Profile
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
            moving_request.status = 'open'
            moving_request.save()
            return redirect("dashboard")
        else:
            print(form.errors)  # For debugging purposes
    else:
        form = MovingRequestForm()

    return render(request, "jobs/create_request.html", {"form": form})

@login_required
def request_list(request):
    """
    Show all moving requests created by the customer.
    """
    requests = MovingRequest.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'jobs/request_list.html', {'requests': requests})

@login_required
def request_detail(request, request_id):
    moving_request = get_object_or_404(
        MovingRequest,
        id=request_id,
        customer=request.user
    )

    bids = moving_request.bids.select_related('mover')

    return render(request, 'jobs/request_detail.html', {
        'request_obj': moving_request,
        'bids': bids
    })

@login_required
def available_jobs(request):
    if request.user.profile.role != 'mover':
        return redirect('dashboard')

    mover_profile = request.user.moverprofile

    jobs = MovingRequest.objects.filter(
        status='open',
        pickup_location__icontains=mover_profile.service_area
    ).order_by('moving_date')

    return render(request, 'jobs/available_jobs.html', {'jobs': jobs})

@login_required
def place_bid(request, request_id):
    if request.user.profile.role != 'mover':
        return redirect('dashboard')

    moving_request = get_object_or_404(MovingRequest, id=request_id, status='open')

    existing_bid = Bid.objects.filter(moving_request=moving_request, mover=request.user).first()
    if existing_bid:
        messages.error(request, "You have already placed a bid on this request.")
        return redirect('available_jobs')

    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.moving_request = moving_request
            bid.mover = request.user
            bid.save()
            return redirect('available_jobs')
    else:
        form = BidForm()

    return render(request, 'jobs/place_bid.html', {
        'form': form,
        'request_obj': moving_request
    })


'''@login_required
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

    return redirect('my_jobs')'''
#THIS IS OBSOLETE, ACCEPTING A JOB IS NOW DONE BY THE CUSTOMER 

@login_required
def my_jobs(request):
    if request.user.profile.role != 'mover':
        return redirect('dashboard')

    jobs = MovingRequest.objects.filter(
        bids__mover=request.user,
        bids__status='accepted',
        status__in=['accepted', 'in_progress', 'completed']
    ).distinct().order_by('-moving_date')

    return render(request, 'jobs/my_jobs.html', {'jobs': jobs})

@login_required
def accept_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)

    if bid.moving_request.customer != request.user:
        return redirect('dashboard')

    if bid.moving_request.status != 'open':
        return redirect('request_detail', request_id=bid.moving_request.id)

    # Accept this bid
    bid.status = 'accepted'
    bid.save()

    # Reject all others
    Bid.objects.filter(
        moving_request=bid.moving_request
    ).exclude(id=bid.id).update(status='rejected')

    # Update request
    bid.moving_request.status = 'accepted'
    bid.moving_request.save()

    return redirect('request_detail', request_id=bid.moving_request.id)

@login_required
def start_job(request, request_id):
    job = get_object_or_404(
        MovingRequest,
        id=request_id,
        bids__mover=request.user,
        bids__status='accepted'
    )

    if job.status == 'accepted':
        job.status = 'in_progress'
        job.save()

    return redirect('my_jobs')

@login_required
def complete_job(request, request_id):
    """
    Mover marks a job as completed.
    """
    if request.user.profile.role != 'mover':
        return redirect('dashboard')

    job = get_object_or_404(
        MovingRequest, 
        id=request_id,
        bids__mover=request.user,
        bids__status='accepted'
        )

    if job.status == 'in_progress':
        job.status = 'completed'
        job.save()

    return redirect('my_jobs')

@login_required
def cancel_request(request, request_id):
    moving_request = get_object_or_404(
        MovingRequest,
        id=request_id,
        customer=request.user
    )

    if moving_request.status in ['open', 'accepted']:
        moving_request.status = 'cancelled'
        moving_request.save()

    return redirect('dashboard')

@login_required
def cancel_bid(request, request_id):
    bid = get_object_or_404(
        Bid,
        id=request_id,
        mover=request.user
    )

    if bid.status in ['pending']:
        bid.status = 'cancelled'
        bid.save()

    return redirect('dashboard')