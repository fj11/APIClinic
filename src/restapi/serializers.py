from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Feature, TestCase, CaseLevel, APIMethod, TestRun, TestResult, TestCaseResult, TestCaseStatus
from taggit.models import Tag

class TagListSerializer(serializers.Serializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')

class CurrentUserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')

class APIMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIMethod
        fields = ("id","name")

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ("id","name")

class CaseLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseLevel
        fields = ('id','name')

class TestCaseStatusSerializer(serializers.ModelSerializer):
    class Meata:
        model = TestCaseStatus
        fields = ("id", "name")

class TestCaseSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    last_modify_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    # tags = TagListSerializer()

    class Meta:
        model = TestCase
        fields = ("id","name","feature","level", "created_by", "request_method", "request_headers",
                  "request_URL", "request_body", "expected_data", "expected_response", "created_date", "last_modify_date", "status")
        depth = 1

class TestRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestRun
        fields = ("id", "name", "created_by", "start_time", "testcases")

class TestResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestResult
        fields = ("id", "start_time", "end_time", "duration", "name",
                  "total_number", "pass_number", "failed_number", "details")
        depth = 2

class TestCaseResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCaseResult
        fields = ("id", "testcase", "result", "reason", "duration", "real_response", "real_status")
        depth = 1

    
