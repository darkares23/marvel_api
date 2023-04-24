from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def get(self, request, format=None):
    return JsonResponse({"message":
    'FUTURE HOME OF AWESOME THINGS'})