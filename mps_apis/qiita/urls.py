from django.conf.urls import url
from qiita.views import UpdatesView, RedirectView


urlpatterns = [
    url(r'^updates/$', UpdatesView.as_view(), name='updates'),
    url(r'^redirect/$', RedirectView.as_view(), name='redirect'),
]