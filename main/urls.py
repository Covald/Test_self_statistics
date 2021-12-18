from django.urls import path, include

from main.api import api

app_name = "main"

urlpatterns = [
    path('api/', api.urls),
]
