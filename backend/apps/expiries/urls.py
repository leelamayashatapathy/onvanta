from django.urls import path

from .views import OverdueExpiriesView, UpcomingExpiriesView

urlpatterns = [
    path('upcoming/', UpcomingExpiriesView.as_view(), name='expiries-upcoming'),
    path('overdue/', OverdueExpiriesView.as_view(), name='expiries-overdue'),
]
