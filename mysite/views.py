from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', context = {})

