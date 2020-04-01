from django.urls import path
from .views import FeatureView, ListTestCaseView, ListCaseLevelView, \
    APIMethodView, TestRunView,TestCaseStatusView, TestResultView

urlpatterns = [

    path('feature/', FeatureView.as_view(), name='feature-all'),
    path('testcase/', ListTestCaseView.as_view(), name='testcase-all'),
    path('caselevel/', ListCaseLevelView.as_view(), name='caselevel-all'),
    path('apimethod/', APIMethodView.as_view(), name='apimethod-all'),
    path('testrun/', TestRunView.as_view(), name='testrun-all'),
    path('testresult/', TestResultView.as_view(), name='testresult-all'),
    path('testcasestatus/', TestCaseStatusView.as_view(), name='testcasestatus-all'),
    ]

