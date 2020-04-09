from django.contrib import admin
from .models import Feature, TestCase, CaseLevel, APIMethod, TestRun, TestCaseStatus, TestCaseResult, TestResult
# Register your models here.

admin.site.register(Feature)
admin.site.register(TestCase) # TO be deleted
admin.site.register(CaseLevel)
admin.site.register(APIMethod)
admin.site.register(TestRun) # TO be deleted
admin.site.register(TestCaseStatus) # TO be deleted
admin.site.register(TestCaseResult) # TO be deleted
admin.site.register(TestResult) # TO be deleted