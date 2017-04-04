from django.shortcuts import render
from django.shortcuts import render, HttpResponse, get_object_or_404,Http404, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .forms import WebsiteRegisterForm
from .models import WebsiteRegister

# Create your views here.
def index(request):

    if request.method == 'POST':

        form = WebsiteRegisterForm(request.POST)

        if form.is_valid():

            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            message = request.POST.get('message')

            print(last_name, first_name, email, phone, message)

            instance = WebsiteRegister(first_name=first_name, last_name=last_name, email=email, phone=phone, message=message)
            instance.save()

            return HttpResponseRedirect(reverse('website:index'))
    else:
        form = WebsiteRegisterForm()

    return render(request, 'website/index.html', {'form': form})


def english(request):
    if request.method == 'POST':

        form = WebsiteRegisterForm(request.POST)

        if form.is_valid():
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            message = request.POST.get('message')

            print(last_name, first_name, email, phone, message)

            instance = WebsiteRegister(first_name=first_name, last_name=last_name, email=email, phone=phone,
                                       message=message)
            instance.save()

            return HttpResponseRedirect(reverse('website:english'))
    else:
        form = WebsiteRegisterForm()

    return render(request, 'website/english.html', {'form': form})

