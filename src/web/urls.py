
from .views import HomePageView, TestPlanPageView, TestRunPageView
from django.urls import path

urlpatterns = [
    path('index', HomePageView.as_view(), name='index'),
    path('test_plan', TestPlanPageView.as_view(), name='test_plan'),
    path('test_run', TestRunPageView.as_view(), name='test_run'),
    ]

