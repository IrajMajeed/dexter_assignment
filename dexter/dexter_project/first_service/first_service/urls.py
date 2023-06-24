from django.conf.urls import include, url
from django.urls import path, re_path
from .views import AudioWaveView

# router = routers.DefaultRouter()


urlpatterns = [
path('audio-wave/',AudioWaveView.as_view()),
]