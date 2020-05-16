# minionserver URL Configuration

from django.urls.conf import include
from django.contrib import admin
from django.urls import path
import minionserver.models as models

urlpatterns = [
    # URL padrão para namespace do minionweb
    path('', include('minionweb.urls', namespace='minionweb')),

    # URL para conexão dos clientes Minions
    path('wordList/', models.getWordList),

    # URL para post dos minions
    path('postResult/', models.postResult),

    # URL para post das Info dos minions
    path('postInfMinion/', models.postInfMinion),

    # URL para Interface administrativa
    path('admin/', admin.site.urls),
]
