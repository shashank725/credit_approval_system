from django.shortcuts import render
from django.http.response import JsonResponse
from celery.result import AsyncResult

from credit_approval_system.celery import celery_app
from api.tasks import ingest_data

# Create your views here.

def import_data(request):
    task = ingest_data.delay()
    result = AsyncResult(task.id, app=celery_app)
    return JsonResponse({task.id:'Uploading to DB'})
