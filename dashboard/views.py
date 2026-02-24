from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from jobs.models import MovingRequest, JobAssignment
from django.db.models import Count

@login_required
def dashboard(request):
    role = request.user.profile.role

    if role == "customer":
        requests = MovingRequest.objects.filter(customer=request.user)

        stats = {
            "total": requests.count(),
            "pending": requests.filter(status='pending').count(),
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
        jobs = JobAssignment.objects.filter(mover=request.user)

        stats = {
            "total": jobs.count(),
            "assigned": jobs.filter(status='assigned').count(),
            "in_progress": jobs.filter(status='in_progress').count(),
            "completed": jobs.filter(status='completed').count(),
            "cancelled": jobs.filter(status='cancelled').count(),
        }

        status_filter = request.GET.get("status")
        if status_filter:
            jobs = jobs.filter(status=status_filter)

        return render(request, "dashboard/mover_dashboard.html", {
            "jobs": jobs.order_by('-assigned_at'),
            "stats": stats,
        })
