# minionserver URL Configuration

from minionweb.views import IndexTemplateView
from django.urls import path

app_name = 'minionweb'

urlpatterns = [
    # GET /
    path('', IndexTemplateView.as_view(), name="index"),

]
