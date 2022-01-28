from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy


from .models import Bd, Rubric
# IMPORT FOR FORMS
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from .forms import BdForm


from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from django.views.generic.list import ListView


############################################ main view   ######################################################
def index(request):
    bbs = Bd.objects.all()
    rubrics = Rubric.objects.all()

    context = {'bbs': bbs, 'rubrics': rubrics}
    return render(request, 'bboard/index.html', context)


###########################################   view item filter by rubric   #######################################
def by_rubric(request, rubric_id): # do not plug in project, it's alternate function class BdByRubricView
    bbs = Bd.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'bboard/by_rubric.html', context)


class BdByRubricView(ListView):
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bd.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubric'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
        return context


""" old version of class
class BdByRubricView(TemplateView):
    template_name = 'bboard/by_rubric.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bbs'] = Bd.objects.filter(rubric=context['rubric_id'])
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
        return context
"""


#############################################  add, edit, delete new items   ###########################################
def add(request):
    bbf = BdForm()
    context = {'form': bbf}
    return render(request, 'bboard/create.html', context)


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


# CONTROLLER-CLASS FORM ----------------------------------------------------------
class BdCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BdForm
    # success_url = '/bboard/'
    success_url = reverse_lazy('index')
    model = Bd

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BdAddView(FormView):
    template_name = 'bboard/create.html'
    form_class = BdForm
    initial = {'price': 0.0}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubric'] = Rubric.objects.all()
        return context

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('bboard:by_rubric', kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})


class BdEditView(UpdateView):
    model = Bd
    form_class = BdForm
    template_name_suffix = '_edit'
    # success_url = '/' # if don't want use get_success_url function

    def get_success_url(self):
        # print(dir(self.object))
        return reverse('bboard:by_rubric', kwargs={'rubric_id': self.object.rubric.pk})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BdDeleteView(DeleteView):
    model = Bd
    # success_url = '/'

    def get_success_url(self):
        # print(dir(self.object))
        return reverse('bboard:by_rubric', kwargs={'rubric_id': self.object.rubric.pk})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

##############################################     details      ####################################
def detail(request, bb_id):
    try:
        bb = Bd.objects.get(pk=bb_id)
        context = {'bbs': bb}
    except Bd.DoesNotExist:
        return HttpResponseNotFound('Такое объявление не существует')
    return render(request, 'bboard/item.html', context)


class BdDetailView(DetailView):
    # default template is "model_detail.html" -> bd_detail.html
    model = Bd

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['rubrics'] = Rubric.objects.all()
        return context

