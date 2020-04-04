
from django.views.generic.base import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.forms import formset_factory
from .forms import TestCaseForm, TestRunForm
from restapi.models import TestResult

# Create your views here.

class HomePageView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        form = AuthenticationForm()
        test_case_form = TestCaseForm()
        # test_case_formset = formset_factory(test_case_form)
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['form'] = form
        context['test_case_form'] = test_case_form
        # context["test_case_formset"] = test_case_formset
        return context

class TestPlanPageView(TemplateView):
    
    template_name = "test_plan.html"

    def get_context_data(self, **kwargs):
        form = AuthenticationForm()
        test_case_form = TestCaseForm()
        # test_case_formset = formset_factory(test_case_form)
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['form'] = form
        context['test_case_form'] = test_case_form
        # context["test_case_formset"] = test_case_formset
        return context

class TestRunPageView(TemplateView):
    template_name = "test_run.html"

    def get_context_data(self, **kwargs):
        form = AuthenticationForm()
        test_results = reversed(TestResult.objects.all())
        test_run = TestRunForm()
        # test_case_formset = formset_factory(test_case_form)
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['form'] = form
        context['test_results'] = test_results
        context['test_run'] = test_run
        # context["test_case_formset"] = test_case_formset
        return context