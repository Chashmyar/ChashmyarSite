from django.urls import path

from accounts import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('logout/', views.logout, name="logout"),
    path('cost/', views.cost, name="cost")
]
