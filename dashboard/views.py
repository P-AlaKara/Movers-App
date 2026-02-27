from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from jobs.models import MovingRequest, Bid
from django.db.models import Count

@login_required
def dashboard(request):
    role = request.user.profile.role

    if role == "customer":
        requests = MovingRequest.objects.filter(customer=request.user)

        stats = {
            "total": requests.count(),
            "open": requests.filter(status='open').count(),
            "accepted": requests.filter(status='accepted').count(),
            "completed": requests.filter(status='completed').count(),
            "cancelled": requests.filter(status='cancelled').count(),
        }

        status_filter = request.GET.get("status")
        if status_filter:
            requests = requests.filter(status=status_filter)

        return render(request, "dashboard/customer_dashboard.html", {
            "requests": requests.order_by('-created_at'),
            "stats": stats,
        })

    elif role == "mover":
        bids = Bid.objects.filter(mover=request.user).select_related('moving_request')
        jobs = MovingRequest.objects.filter(bids__mover=request.user, bids__status='accepted').distinct()

        job_stats = {
            "total": jobs.count(),
            "open": jobs.filter(status='open').count(),
            "accepted": jobs.filter(status='accepted').count(),
            "in_progress": jobs.filter(status='in_progress').count(),
            "completed": jobs.filter(status='completed').count(),
            "cancelled": jobs.filter(status='cancelled').count(),
        }

        bid_stats = {
            "total": bids.count(),
            "pending": bids.filter(status='pending').count(),
            "accepted": bids.filter(status='accepted').count(),
            "rejected": bids.filter(status='rejected').count(),
            "cancelled": bids.filter(status='cancelled').count(),
        }

        stats = {
            "job_stats": job_stats,
            "bid_stats": bid_stats
        }

        status_filter = request.GET.get("status")
        if status_filter:
            jobs = jobs.filter(status=status_filter)

        return render(request, "dashboard/mover_dashboard.html", {
            "jobs": jobs.order_by('-moving_date'),
            "stats": stats,
        })
