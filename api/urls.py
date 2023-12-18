from django.urls import path
from api.views import import_data


urlpatterns = [
    path('import_data/', import_data, name="import_data"),
]