from django.urls import path
from .views import numerology_full_analysis, get_numerology_report

urlpatterns = [
    path('api/numerology/', numerology_full_analysis, name='numerology_post'),
    path('api/report/<str:public_id>/', get_numerology_report, name='numerology_report'),
]