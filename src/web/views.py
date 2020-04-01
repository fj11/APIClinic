
from django.views.generic.base import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.forms import formset_factory
from .forms import TestCaseForm

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