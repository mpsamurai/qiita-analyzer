from django.conf.urls import url
from qiita.views import UpdatesView


urlpatterns = [
    url(r'^updates/$', UpdatesView.as_view(), name='updates'),
]