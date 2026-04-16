from django.urls import include, path

urlpatterns = [
    path('auth/', include('apps.accounts.urls')),
    path('organizations/', include('apps.organizations.urls')),
    path('vendors/', include('apps.vendors.urls')),
    path('vendors/', include('apps.vendor_documents.vendor_urls')),
    path('document-types/', include('apps.document_types.urls')),
    path('onboarding/', include('apps.onboarding.urls')),
    path('documents/', include('apps.vendor_documents.urls')),
    path('audit/', include('apps.auditlog.urls')),
    path('approvals/', include('apps.approvals.urls')),
    path('expiries/', include('apps.expiries.urls')),
    path('tasks/', include('apps.tasks.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('platform-admin/', include('apps.platform_admin.urls')),
    path('setup/', include('apps.organization_setup.urls')),
]
