from django.urls import path, include

from webservice import views

urlpatterns = [
    path('virtual-glass/', include('virtualglass.urls')),
    path('eye-care', views.eye_care, name="eye-care"),
    path('info-dashboard', views.info_dashboard, name="info-dashboard")
]