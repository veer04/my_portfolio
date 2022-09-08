from pyexpat import model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, response
from django.core.paginator import Paginator

from veer import models
# Create your views here.
from .forms import create_person_form



def home(request):
    form = create_person_form()

    error = 'Errors in the form, please verify.'

    context = {
        
    }

    if request.method == 'POST':
        form = create_person_form(request.POST)
        #print(form.cleaned_data['Name'])
        if form.is_valid():
            form.save()
            return redirect('success', form.instance.id)
        else:
            context['error'] = error

    context['form'] = form

    all_data = models.Person.objects.all().order_by('-date')
    context['datas'] = all_data

    return render(request, 'veer/index.html', context)


def success(request, pk):
    obj = models.Person.objects.get(pk=pk)
    context = {
        'name': obj.name
    }
    return render(request, 'veer/success.html', context)

def blog(request):
    all_data = models.Person.objects.all().order_by('-date')
    context = {
        'datas' : all_data
    }

    paginator = Paginator(all_data, 9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['page_obj'] = page_obj

    return render(request, 'veer/blog-minibar.html', context)