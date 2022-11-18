from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from blango_auth.forms import BlangoRegistrationForm
@login_required
def profile(request):
    return render(request, "blango_auth/profile.html")

