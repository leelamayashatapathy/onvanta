from django.urls import path

from .views import (
    OnboardingBlockedCasesView,
    OnboardingCaseChecklistView,
    OnboardingCaseDetailView,
    OnboardingCaseStartView,
    OnboardingCaseSubmitApprovalView,
    OnboardingCaseSubmitView,
    OnboardingPendingQueueView,
    OnboardingTemplateDetailView,
    OnboardingTemplateListCreateView,
    OnboardingTemplateRequirementListCreateView,
)

urlpatterns = [
    path('templates/', OnboardingTemplateListCreateView.as_view(), name='onboarding-template-list-create'),
    path('templates/<uuid:template_id>/', OnboardingTemplateDetailView.as_view(), name='onboarding-template-detail'),
    path(
        'templates/<uuid:template_id>/requirements/',
        OnboardingTemplateRequirementListCreateView.as_view(),
        name='onboarding-template-requirements',
    ),
    path('cases/start/', OnboardingCaseStartView.as_view(), name='onboarding-case-start'),
    path('cases/<uuid:case_id>/', OnboardingCaseDetailView.as_view(), name='onboarding-case-detail'),
    path(
        'cases/<uuid:case_id>/checklist/',
        OnboardingCaseChecklistView.as_view(),
        name='onboarding-case-checklist',
    ),
    path('cases/<uuid:case_id>/submit/', OnboardingCaseSubmitView.as_view(), name='onboarding-case-submit'),
    path(
        'cases/<uuid:case_id>/submit-approval/',
        OnboardingCaseSubmitApprovalView.as_view(),
        name='onboarding-case-submit-approval',
    ),
    path('cases/pending/', OnboardingPendingQueueView.as_view(), name='onboarding-case-pending'),
    path('cases/blocked/', OnboardingBlockedCasesView.as_view(), name='onboarding-case-blocked'),
]
