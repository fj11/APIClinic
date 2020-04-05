
from django.forms import ModelForm
from restapi.models import TestCase, TestResult, TestRun

class TestCaseForm(ModelForm):
    class Meta:
        model = TestCase
        fields = ("name", "feature", "level", "status", "request_method", "request_headers",
                  "request_URL", "request_body", "expected_data", "expected_response")

class TestResultForm(ModelForm):
    class Meta:
        model = TestResult
        fields = ("start_time", "end_time", "duration",
                  )

class TestRunForm(ModelForm):
    class Meta:
        model = TestRun
        fields = ("feature", "level", "status", "request_method")