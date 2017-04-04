from django.shortcuts import render
from django.shortcuts import render, HttpResponse, get_object_or_404,Http404, redirect

# Create your views here.
def index(request):
    return render(request, 'website/index.html')

def english(request):
    return render(request, 'website/english.html')