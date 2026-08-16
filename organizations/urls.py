from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('add/', views.add_organization, name='add_organization'),
    path('org/<uuid:org_id>/', views.organization_detail, name='org_detail'),
    path('org/<uuid:org_id>/qr.png', views.organization_qr, name='organization_qr'),
    path('org/<uuid:org_id>/edit/', views.edit_organization, name='edit_organization'),
    path('org/<uuid:org_id>/delete/', views.delete_organization, name='delete_organization'),
    path('feedback/<uuid:org_id>/', views.submit_feedback, name='submit_feedback'),
    path('feedback/success/', views.feedback_success, name='feedback_success'),
]
