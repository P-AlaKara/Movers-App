from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from profiles.models import MoverProfile


# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            role = form.cleaned_data.get("role")
            user.profile.role = role
            user.profile.save()

            if role == 'mover':
                MoverProfile.objects.create(user=user)

            login(request, user)
            return redirect('dashboard')  # Redirect to a success page after registration
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})