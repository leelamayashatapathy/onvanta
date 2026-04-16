from django.urls import path

from .views import DocumentTypeDetailView, DocumentTypeListCreateView

urlpatterns = [
    path('', DocumentTypeListCreateView.as_view(), name='document-type-list-create'),
    path('<uuid:document_type_id>/', DocumentTypeDetailView.as_view(), name='document-type-detail'),
]
