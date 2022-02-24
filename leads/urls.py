from unicodedata import name
from django.urls import path

from leads.views import (
    lead_create,
    lead_delete,
    lead_detail,
    lead_list,
    lead_update,
    LeadListView,
    LeadDetailView,
    LeadCreateView,
    LeadUpdateView,
    LeadDeleteView,
)

app_name = 'leads'
urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('create/', LeadCreateView.as_view(), name='lead-create'),
]
