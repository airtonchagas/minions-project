
from django.views.generic import TemplateView

# Create your views here.


class IndexTemplateView(TemplateView):
    # view do portal web Minion Server
    template_name = "index.html"
