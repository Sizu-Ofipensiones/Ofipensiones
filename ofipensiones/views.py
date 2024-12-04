from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ofipensiones.auth0Backend import getRole


@login_required
def home(request):
    return render(request, 'base.html')