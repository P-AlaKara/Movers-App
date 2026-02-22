from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, MoverProfileForm
from .models import MoverProfile


@login_required
def my_profile(request):
    profile = request.user.profile

    mover_profile = None
    mover_form = None

    if profile.role == 'mover':
        mover_profile = MoverProfile.objects.get(user=request.user)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)

        if mover_profile:
            mover_form = MoverProfileForm(request.POST, instance=mover_profile)
            if profile_form.is_valid() and mover_form.is_valid():
                profile_form.save()
                mover_form.save()
                return redirect('my-profile')
        else:
            if profile_form.is_valid():
                profile_form.save()
                return redirect('my-profile')
    else:
        profile_form = ProfileForm(instance=profile)
        if mover_profile:
            mover_form = MoverProfileForm(instance=mover_profile)

    return render(request, 'profiles/my_profile.html', {
        'profile_form': profile_form,
        'mover_form': mover_form,
        'profile': profile
    })

