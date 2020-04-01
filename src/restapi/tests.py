from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Feature, CaseLevel, TestCase, APIMethod
from .serializers import FeatureSerializer, CaseLevelSerializer
from django.core.exceptions import ObjectDoesNotExist
# Create your tests here.

class BasiViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_test_suite(name=''):
        if name != '':
            Feature.objects.create(name=name)

    @staticmethod
    def delete_test_suite(name=''):
        if name != '':
            try:
                Feature.objects.get(name=name).delete()
            except ObjectDoesNotExist:
                pass

    @staticmethod
    def create_caselevel(name=''):
        if name != '':
            CaseLevel.objects.create(name=name)

    @staticmethod
    def delete_caselevel(name=''):
        if name != '':
            try:
                CaseLevel.objects.get(name=name).delete()
            except ObjectDoesNotExist:
                pass

    def init_testsuite(self):
        self.create_test_suite("testsuite1")
        self.create_test_suite("testsuite2")
        self.create_test_suite("testsuite3")
        self.create_test_suite("testsuite4")

    def init_caselevel(self):
        self.create_caselevel("l1")
        self.create_caselevel("l2")
        self.create_caselevel("l3")

    @classmethod
    def setUpClass(cls):
        cls.init_testsuite(cls)
        cls.init_caselevel(cls)

    def setUp(self):
        # self.init_testsuite()
        # self.init_caselevel()
        pass

    def tearDown(self):
        # self.clear_testsuite()
        # self.clear_caselevel()
        pass

    @classmethod
    def tearDownClass(cls):
        cls.clear_caselevel(cls)
        cls.clear_testsuite(cls)

    def clear_testsuite(self):
        self.delete_test_suite("testsuite1")
        self.delete_test_suite("testsuite2")
        self.delete_test_suite("testsuite3")
        self.delete_test_suite("testsuite4")
        self.delete_test_suite("testsuite5")
        self.delete_test_suite("testsuite6")
        self.delete_test_suite("testsuite7")
        self.delete_test_suite("testsuite8")

    def clear_caselevel(self):
        self.delete_caselevel("l1")
        self.delete_caselevel("l2")
        self.delete_caselevel("l3")
        self.delete_caselevel("l4")
        self.delete_caselevel("l5")
        self.delete_caselevel("l6")
        self.delete_caselevel("l7")

class CaseLevels(BasiViewTest):

    def test_get_all_caselevel(self):
        self.create_test_suite("testsuite1")
        self.create_test_suite("testsuite2")
        response = self.client.get(reverse("caselevel-all"))
        expected = CaseLevel.objects.all()
        serialized = CaseLevelSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_caselevel_by_id(self):
        self.create_test_suite("testsuite1")
        self.create_test_suite("testsuite2")
        caselevel = CaseLevel.objects.all()[0]
        id = caselevel.id
        serialized = CaseLevelSerializer(caselevel, many=False)
        response = self.client.get("http://127.0.0.1:8000/caselevel/?id=%s" % id)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_caselevel(self):
        response = self.client.post("http://127.0.0.1:8000/caselevel/", data={"name": "l4"})
        caselevel = CaseLevel.objects.get(name="l4")
        serialized = CaseLevelSerializer(caselevel, many=False)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_caselevel(self):
        self.create_caselevel("l5")
        caselevel = CaseLevel.objects.get(name="l5")
        id = caselevel.id
        response = self.client.delete("http://127.0.0.1:8000/caselevel/", data={"id": id})
        self.assertEqual(response.data, "Delete Success")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_caselevel(self):
        self.create_caselevel("l6")
        caselevel = CaseLevel.objects.get(name="l6")
        id = caselevel.id
        caselevel.name = "l7"
        serialized = CaseLevelSerializer(caselevel, many=False)
        response = self.client.put("http://127.0.0.1:8000/caselevel/", data={"id": id, "name":"l7"})
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

class TestSuites(BasiViewTest):

    def test_get_all_testsuites(self):
        response = self.client.get(reverse("testsuite-all"))
        expected = Feature.objects.all()
        serialized = FeatureSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_testsuite_by_id(self):
        testsuite = Feature.objects.all()[0]
        id = testsuite.id
        serialized = FeatureSerializer(testsuite, many=False)
        response = self.client.get("http://127.0.0.1:8000/testsuite/?id=%s" % id)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_testsuite(self):
        response = self.client.post("http://127.0.0.1:8000/testsuite/", data={"name": "testsuite5"})
        testsuite = Feature.objects.get(name="testsuite5")
        serialized = FeatureSerializer(testsuite, many=False)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_testsuite(self):
        self.create_test_suite("testsuite6")
        testsuite = Feature.objects.get(name="testsuite6")
        id = testsuite.id
        response = self.client.delete("http://127.0.0.1:8000/testsuite/", data={"id": id})
        self.assertEqual(response.data, "Delete Success")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_testsuite(self):
        self.create_test_suite("testsuite7")
        testsuite = Feature.objects.get(name="testsuite7")
        id = testsuite.id
        testsuite.name = "testsuite8"
        serialized = FeatureSerializer(testsuite, many=False)
        response = self.client.put("http://127.0.0.1:8000/testsuite/", data={"id": id, "name":"testsuite8"})
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
