
from django.forms import ModelForm
from restapi.models import TestCase

class TestCaseForm(ModelForm):
    class Meta:
        model = TestCase
        fields = ("name", "feature", "level", "status", "request_method", "request_headers",
                  "request_URL", "request_body", "expected_data", "expected_response")