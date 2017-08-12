from django.shortcuts import render
from qiita import models
# Create your views here.
from django.views import View

# コマンドラインをスクリプトから実行
import subprocess



class UpdatesView(View):

    def get(self, request):
        subprocess.call('./qiita_module_execution.sh')
        return render(request, 'qiita/data_update.html', {})