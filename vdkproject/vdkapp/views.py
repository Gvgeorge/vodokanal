from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import Order


class IndexView(View):
    def get(self, request):
        qs = Order.objects.all()
        return JsonResponse({'orders': list(qs.values())})
