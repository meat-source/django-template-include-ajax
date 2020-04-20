from django.http import HttpResponse
from django.shortcuts import render
from django.template import TemplateDoesNotExist


def include_ajax(request, template):
    template = template.replace('&', '/')  # для шаблонов вложенных в папку
    try:
        return render(request, template)
    except TemplateDoesNotExist:
        return HttpResponse(status=404)


# Create your views here.
def demo(request):
    return render(request, 'index.html')