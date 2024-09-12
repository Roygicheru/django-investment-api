from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def user_profile(request):
    user = request.user
    # Retrieve any additional user data or perform necessary operations
    context = {
        'user': user,
        # Add any additional context data to pass to the template
    }
    return render(request, 'accounts/profile.html', context)
