from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('inscription/<int:pk>/edit/', views.edit_inscription, name='edit_inscription'),
    path('inscription/<int:pk>/cancel/', views.cancel_inscription, name='cancel_inscription'),
    path('report/', views.inscription_report, name='inscription_report'),
    path('report/export/', views.export_inscriptions_csv, name='export_inscriptions_csv'),
]