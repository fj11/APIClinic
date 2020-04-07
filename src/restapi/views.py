
from django.core import serializers
from django.http import JsonResponse
import datetime
from .models import Feature, TestCase, CaseLevel, APIMethod, TestRun,\
    TestResult, TestCaseResult, TestCaseStatus
from .serializers import FeatureSerializer, TestCaseSerializer, \
    CaseLevelSerializer, APIMethodSerializer, TestRunSerializer, TestResultSerializer, TestCaseResultSerializer, TestCaseStatusSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import status
from django.core.exceptions import ObjectDoesNotExist
from .lib.testEngine import start
from .lib import loadEngine
from multiprocessing import Pool, cpu_count
from django.db.models import Q
from model_utils import Choices
import json
import copy

# Create your views here.

ORDER_COLUMN_CHOICES = Choices(
    ('0', 'id'),
    ('1', 'name'),
    ('2', 'feature'),
    ('3', 'level'),
    ('4', 'request_method'),
    ('5', 'created_by'),
    ('6', 'action')
)

class APIMethodView(APIView):
    def get(self, request):
        requestParams = request.query_params
        if "id" in requestParams:
            method = APIMethod.objects.get(id=requestParams["id"])
            serialized = APIMethodSerializer(method, many=False)
        else:
            method = APIMethod.objects.all()
            serialized = APIMethodSerializer(method, many=True)
        return Response(serialized.data)

    def post(self, request):
        serializer = APIMethodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        if "id" not in request.data:
            return Response("Id not found", status=status.HTTP_400_BAD_REQUEST)
        obj, created = APIMethod.objects.update_or_create(id=request.data["id"],
                                                          defaults={'name': request.data["name"]})
        obj.save()
        serialized = APIMethodSerializer(obj, many=False)
        if created:
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request):
        if "id" not in request.data:
            return Response("Id not found", status=status.HTTP_400_BAD_REQUEST)
        method = APIMethod.objects.get(id=request.data["id"])
        method.delete()
        return Response("Delete Success")

class FeatureView(APIView):

    def get(self, request):
        requestParams = request.query_params
        if "id" in requestParams:
            testsuites = Feature.objects.get(id=requestParams["id"])
            serialized = FeatureSerializer(testsuites, many=False)
        else:
            testsuites = Feature.objects.all()
            serialized = FeatureSerializer(testsuites, many=True)
        return Response(serialized.data)

    def post(self, request):
        testsuite = Feature.objects.create(data=request.data)
        serializer = FeatureSerializer(testsuite)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        if "id" not in request.data:
            return Response("Id not found", status=status.HTTP_400_BAD_REQUEST)
        obj, created = Feature.objects.update_or_create(id=request.data["id"],
                                                        defaults={'name': request.data["name"]})
        obj.save()
        serialized = FeatureSerializer(obj, many=False)
        if created:
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request):
        if "id" not in request.data:
            return Response("Id not found", status=status.HTTP_400_BAD_REQUEST)
        testsuites = Feature.objects.get(id=request.data["id"])
        testsuites.delete()
        return Response("Delete Success")

class ListTestCaseView(APIView):
    def get(self, request):
        requestParams = request.query_params
        if "id" in requestParams:
            testcase = TestCase.objects.get(id=requestParams["id"])
            serialized = TestCaseSerializer(testcase, many=False)
            return Response(serialized.data)
        else:
            testcase = TestCase.objects.all()
            if "draw" not in requestParams:
                serialized = TestCaseSerializer(testcase, many=True)
                return Response(serialized.data)
            draw = int(requestParams.get('draw', 0))

            length = int(requestParams.get('length', 0))
            start = int(requestParams.get('start', 0))
            search_value = requestParams.get('search[value]', 0)
            order_column = requestParams.get('order[0][column]', 0)
            order = requestParams.get('order[0][dir]', 0)

            order_column = ORDER_COLUMN_CHOICES[order_column] if int(order_column) < 5 else None
            # django orm '-' -> desc
            if order == 'desc' and order_column:
                order_column = '-' + order_column
            total = testcase.count()
            if search_value:
                testcase = testcase.filter(Q(name__icontains=search_value) |
                                           Q(level__name__icontains=search_value) |
                                           Q(request_method__name__icontains=search_value) |
                                           Q(feature__name__icontains=search_value) |
                                           Q(created_by__username__icontains=search_value)
                                           )

            count = testcase.count()
            if order_column:
                testcase = testcase.order_by(order_column)[start:start + length]
            result = {
                'data': TestCaseSerializer(testcase, many=True).data,
                'recordsFiltered': count,
                'recordsTotal': total,
                'draw': draw
            }
            return Response(result)

    def post(self, request):

        data = copy.deepcopy(request.data)
        caselevel = CaseLevel.objects.get(id=data["level"])
        method = APIMethod.objects.get(id=data["request_method"])
        feature = Feature.objects.get(id=data["feature"])
        test_case_status = TestCaseStatus.objects.get(id=data["status"])
        test_case = TestCase.objects.create(
                                                name=data["name"],
                                                feature=feature,
                                                level=caselevel,
                                                status=test_case_status,
                                                request_method=method,
                                                request_headers=data["request_headers"],
                                                request_URL=data["request_URL"],
                                                request_body=data["request_body"],

                                                expected_data= data["expected_data"],
                                                expected_response=data["expected_response"],


                                        )
        serialized = TestCaseSerializer(test_case, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):

        data = copy.deepcopy(request.data)
        
        params = request.query_params
        if "id" not in data and "id" not in params: 
            return Response("Id not found", status=status.HTTP_400_BAD_REQUEST)
        id = data["id"] if "id" in data else params['id']
        if "level" in data:
            caselevel = CaseLevel.objects.get(id=data["level"])
            data["level"] = caselevel
        if "request_method" in data:
            method = APIMethod.objects.get(id=data["request_method"])
            data["request_method"] = method
        if "feature" in data:
            suite = Feature.objects.get(id=data["feature"])
            data["feature"] = suite
        if "status" in data:
            testcaseStatus = TestCaseStatus.objects.get(id=data["status"])
            data["status"] = testcaseStatus
        obj, created = TestCase.objects.update_or_create(id=id,
                                                          defaults=data)
        obj.save()
        serialized = TestCaseSerializer(obj, many=False)
        if created:
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request):
        if "id" not in request.query_params:
            return Response("Id not found", status=status.HTTP_400_BAD_REQUEST)
        testcase = TestCase.objects.get(id=request.query_params["id"])

        testcase.delete()
        return Response("Delete Success")

class ListCaseLevelView(APIView):

    def get(self, request):
        requestParams = request.query_params
        if "id" in requestParams:
            caselevels = CaseLevel.objects.get(id=requestParams["id"])
            serialized = CaseLevelSerializer(caselevels, many=False)
        else:
            caselevels = CaseLevel.objects.all()
            serialized = CaseLevelSerializer(caselevels, many=True)
        return Response(serialized.data)

    def post(self, request):
        serializer = CaseLevelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        if "id" not in request.data:
            return Response("Id not found", status=status.HTTP_400_BAD_REQUEST)
        obj, created = CaseLevel.objects.update_or_create(id=request.data["id"],defaults={'name': request.data["name"]})
        obj.save()
        serialized = CaseLevelSerializer(obj, many=False)
        if created:
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request):
        if "id" not in request.data:
            return Response("Id not found", status=status.HTTP_400_BAD_REQUEST)
        testsuites = CaseLevel.objects.get(id=request.data["id"])
        testsuites.delete()
        return Response("Delete Success")

class TestRunView(APIView):
    def get(self, request):
        requestParams = request.query_params
        if "id" in requestParams:
            testrun = TestRun.objects.get(id=requestParams["id"])
            serialized = TestRunSerializer(testrun, many=False)
        else:
            testrun = TestRun.objects.all()
            serialized = TestRunSerializer(testrun, many=True)
        return Response(serialized.data)

    def post(self, request):
        
        data = copy.deepcopy(request.data)
        testResultList = list(TestResult.objects.all())
        while len(testResultList) > 9:
            tc = testResultList.pop(0)
            if tc.id is not None:
                tc.delete()
        testcases = []
        if "testcases" in data:
            testcase_id = data["testcases"].split(",")
            testcases = TestCase.objects.filter(id__in=testcase_id).values( "id",
                                                                        "request_method__name", 
                                                                        "expected_response", 
                                                                        "request_body",
                                                                        "expected_response",
                                                                        "expected_data",
                                                                        "request_headers",
                                                                        "status__name",
                                                                        "request_URL")
        else:
            testcases = TestCase.objects.all()
            if data['level'] != '---------':
                testcases = testcases.filter(level__name=data['level'])
            
            if data['request_method'] != '---------':
                testcases = testcases.filter(request_method__name=data['request_method'])
            
            if data['feature'] != '---------':
                testcases = testcases.filter(feature__name=data['feature'])
            if data['status'] != '---------':
                testcases = testcases.filter(status__name=data['status'])

            testcases = testcases.values( "id",
                                                                        "request_method__name", 
                                                                        "expected_response", 
                                                                        "request_body",
                                                                        "expected_response",
                                                                        "expected_data",
                                                                        "request_headers",
                                                                        "status__name",
                                                                        "request_URL")
        start_time = datetime.datetime.now()
        if data['type'] == "functional":
            pool = Pool(processes=cpu_count())
            results = pool.map(start, list(testcases))
            # print(results)
            pool.close()
            pool.join()
            test_case_result_model = []
            for result in results:
                t = TestCaseResult.objects.create(
                    testcase = TestCase.objects.get(id=result['id']),
                    result = result['result'],
                    reason = result['reason'],
                    real_status = result['real_status'],
                    real_response = result['real_response'],
                    duration = result['duration']
                )
                test_case_result_model.append(t)
            
            totalNumber = len(results)
            passNumber = len([i for i in results if i["result"] == "PASS"])
            failedNumber = totalNumber - passNumber
            end_time = datetime.datetime.now()
            test_result_model = TestResult.objects.create(
                    start_time = start_time,
                    end_time = end_time,
                    duration = end_time - start_time,
                    total_number = totalNumber,
                    pass_number = passNumber,
                    failed_number = failedNumber,
                    result_type = "Functional"
            )
            test_result_model.details.set(test_case_result_model)
            serializer = TestResultSerializer(test_result_model, many=False)
        elif data['type'] == "performance":
            data['start_time'] = start_time
            results = loadEngine.start(testcases, data)
            test_case_result_model = []
            for result in results:
                t = TestCaseResult.objects.create(
                    testcase = TestCase.objects.get(id=result['id']),
                    result = "PASS" if result['response_code'].keys() == 1 and result['response_code'].keys()[0] == 200 else "FAILED",
                    real_status = result['response_code'],
                    real_response = result['response_number'],
                    duration = datetime.timedelta(seconds=result['response_time'])
                )
                test_case_result_model.append(t)
            end_time = datetime.datetime.now()
            test_result_model = TestResult.objects.create(
                    start_time = start_time,
                    end_time = end_time,
                    duration = end_time - start_time,
                    total_number = len(results),
                    pass_number = 0,
                    failed_number = 0,
                    result_type = "Performance"
            )
            test_result_model.details.set(test_case_result_model)
            serializer = TestResultSerializer(test_result_model, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        if "id" not in request.data:
            return Response("Id not found", status=status.HTTP_400_BAD_REQUEST)
        testrun = TestRun.objects.get(id=request.data["id"])
        testrun.delete()
        return Response("Delete Success")

class TestCaseStatusView(APIView):
    pass

class TestCaseResultView(APIView):
    def get(self, request):
        requestParams = request.query_params
        if "id" in requestParams:
            testcaseresult = TestCaseResult.objects.get(id=requestParams["id"])
            serialized = TestCaseResultSerializer(testcaseresult, many=False)
        else:
            testcaseresult = TestCaseResult.objects.all()
            serialized = TestCaseResultSerializer(testcaseresult, many=True)
        return Response(serialized.data)

class TestResultView(APIView):
    def get(self, request):
        requestParams = request.query_params
        depth = requestParams['depth'] if 'depth' in requestParams else 1
        if "id" in requestParams:
            testresult = TestResult.objects.get(id=requestParams["id"])
            serialized = TestResultSerializer(testresult, many=False)
        else:
            testresult = TestResult.objects.all()
            serialized = TestResultSerializer(testresult, many=True)
        return Response(serialized.data)
