from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse


class IndexView(generic.TemplateView):
    template_name = 'segments/index.html'


class ResultView(generic.DetailView):
    template_name = 'segments/result.html'


def check_intersection(request):
    print(request.POST['ax'])
    print(request.POST['ay'])
    print(request.POST['bx'])
    print(request.POST['by'])
    print(request.POST['cx'])
    print(request.POST['cy'])
    print(request.POST['dx'])
    print(request.POST['dy'])
    return HttpResponseRedirect(reverse('segments:index'))
