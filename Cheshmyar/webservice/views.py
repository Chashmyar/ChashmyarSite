from django.shortcuts import render
import pages.views


# Create your views here.
def webservice(request):
    return render(request, 'service.html', {'is_logged_in': pages.views.is_logged_in})



def eye_care(request):
    return render(request, 'services/eye-care.html', {'is_logged_in': pages.views.is_logged_in})


def info_dashboard(request):
    return render(request, 'services/info-dashboard.html', {'is_logged_in': pages.views.is_logged_in})
