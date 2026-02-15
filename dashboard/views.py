from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def dashboard_view(request):
    role = request.user.profile.role

    if role == "mover":
        return render(request, "dashboard/mover_dashboard.html")

    return render(request, "dashboard/customer_dashboard.html")
