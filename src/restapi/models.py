from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django.db import models
from taggit.managers import TaggableManager
from django_currentuser.db.models import CurrentUserField
from django.contrib.auth.models import User
from treebeard.al_tree import AL_Node
import uuid
import datetime
# Create your models here.

class APIMethod(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.name

class CaseLevel(models.Model):

    name = models.CharField(max_length=10, blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.name

class Feature(models.Model):

    name = models.CharField(max_length=255, blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return "{}".format(self.name)

class TestCaseStatus(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return "{}".format(self.name)

class TestCase(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    name = models.CharField(max_length=255, blank=True, null=True)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, blank=True, null=True)
    level = models.ForeignKey(CaseLevel, on_delete=models.CASCADE, blank=True, null=True)
    created_by = CurrentUserField(editable=False, on_delete=models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(TestCaseStatus, on_delete=models.CASCADE, blank=True, null=True)
    # tags = TaggableManager(blank=True)

    created_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    last_modify_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    request_method = models.ForeignKey(APIMethod, on_delete=models.CASCADE, blank=True, null=True)
    request_headers = models.TextField(blank=True, default="")
    request_URL = models.URLField(max_length=255, default="")
    request_body = models.TextField(blank=True, default="")
    expected_response = models.TextField(blank=True, default="")
    expected_data = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name

class TestRun(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    start_time = models.DateTimeField(auto_now=True, auto_now_add=False)
    name = models.CharField(max_length=255, default="Run API Testing At: %s" % datetime.datetime.now().strftime("%c"),
                            editable=False)
    created_by = models.ForeignKey(User, null=True, editable=False, on_delete=models.CASCADE)
    level = models.ForeignKey(CaseLevel, on_delete=models.CASCADE, null=True)
    status = models.ForeignKey(TestCaseStatus, on_delete=models.CASCADE, null=True)
    request_method = models.ForeignKey(APIMethod, on_delete=models.CASCADE, null=True)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, null=True)
    testcases = models.ManyToManyField(TestCase)

    def __str__(self):
        return self.name

class TestCaseResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    testcase = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    result = models.CharField(max_length=10, null=True)
    reason = models.TextField(max_length=255, null=True)
    real_status = models.CharField(max_length=100, default='')
    real_response = models.TextField(max_length=10000, default='')
    duration = models.DurationField(null=True)

    status_code_success = models.IntegerField(default=0, null=True)
    status_code_client_error = models.IntegerField(default=0, null=True)
    status_code_server_error = models.IntegerField(default=0, null=True)
    request_total_number = models.IntegerField(default=0, null=True)
    response_time = models.DurationField(null=True)

    class Meta:
        ordering = ['result']

class TestResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField(max_length=100, null=True)
    name = models.CharField(max_length=255, default="Result At: %s" % datetime.datetime.now().strftime("%c"),
                            editable=False)
    total_number = models.IntegerField(editable=False, default=0)
    pass_number = models.IntegerField(editable=False, default=0)
    failed_number = models.IntegerField(editable=False, default=0)
    result_type = models.CharField(max_length=20, default="Functional")
    details = models.ManyToManyField(TestCaseResult)

    class Meta:
        ordering = ['start_time']
