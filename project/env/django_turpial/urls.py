#   DJANGO IMPORTS
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/',admin.site.urls),
    path('', include('eval_test.urls')),
]
