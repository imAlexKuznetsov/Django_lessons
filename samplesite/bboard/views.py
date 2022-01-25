from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Bd, Rubric
# IMPORT FOR FORMS
from django.views.generic.edit import CreateView
from .forms import BdForm


# Create your views here.
def index(request):
    bbs = Bd.objects.all()
    rubrics = Rubric.objects.all()
    context = {'bbs': bbs, 'rubrics': rubrics}
    return render(request, 'bboard/index.html', context)


def by_rubric(request, rubric_id):
    bbs = Bd.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'bboard/by_rubric.html', context)


# CONTROLLER-CLASS FORM
class BdCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BdForm
    success_url = '/bboard/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


def add(request):
    bbf = BdForm()
    context = {'form': bbf}
    return render(request, 'bboard/create.html', context)
#
#
# def add_save(request):
#     bbf = BdForm(request.POST)
#     if bbf.is_valid():
#         bbf.save()
#         return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
#     else:
#         context = {'form': bbf}
#         return render(request, 'bboard/')


def add_and_save(request):
    if request.method == 'POST':
        bbf = BdForm(request.POST)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse('bboard:by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
    else:
        bbf = BdForm()
        context = {'form': bbf}
        return render(request, 'bboard/create.html', context)
