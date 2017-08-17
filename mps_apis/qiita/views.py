from django.shortcuts import render
from qiita import models
# Create your views here.
from django.views import View
# コマンドラインをスクリプトから実行
import subprocess
import urllib.request, urllib.parse



class UpdatesView(View):



    def get(self, request):
        subprocess.call('./qiita_module_execution.sh')
        # GET /api/v2/oauth/authorize へ client_idとscopeでアクセス『許可』画面へのURL
        page = "https://qiita.com/api/v2/oauth/authorize?client_id=5ac39514be164adfe85e9df3defc7ca5e791adc9&scope=read_qiita"
        return render(request, 'qiita/data_update.html', {
            'page': page
        })


class RedirectView(View):

    def get(self, request):
        return render(request, 'qiita/redirect.html', {})
