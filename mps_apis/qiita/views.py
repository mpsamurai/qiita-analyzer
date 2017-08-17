from django.shortcuts import render
from qiita import models
# Create your views here.
from django.views import View
# コマンドラインをスクリプトから実行
import subprocess
import urllib.request, urllib.parse
import json



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
        if "code" in request.GET:
            # query_paramが指定されている場合の処理( codeを取得 )
            param_value = request.GET.get("code")

            data = {
                "client_id": "5ac39514be164adfe85e9df3defc7ca5e791adc9",
                "client_secret": "196628b368ffddaa232725109e377b11d4093882",
                "code": param_value
            }
            json_data = json.dumps(data).encode("utf-8")
            url = "https://qiita.com/api/v2/access_tokens"
            method = "POST"
            headers = {"Content-Type": "application/json"}

        req = urllib.request.Request(url, data=json_data, method=method, headers=headers)
        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode("utf-8")
        # print("param_value", param_value)
        return render(request, 'qiita/redirect.html', {
            'response_body': response_body
        })
