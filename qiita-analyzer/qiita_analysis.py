# django-qiita-analyzerモジュールをimportしてdjangoモデル使う
# localファイル.bash_profile
# MPSのdjango-qiita-analyzerパス
# export DJANGO_QIITA_ANALYZER=/Users/hiroshiteraoka/MPS/mps_website/django-qiita-analyzer/mps_apis

import os, sys
import MeCab

# このファイル実行前に一度上記exportをコマンドラインでパス通す
django_qiita_analyzer = os.environ['DJANGO_QIITA_ANALYZER']
sys.path.append(django_qiita_analyzer)  # med_m_tool_web へのパス
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mps_apis.settings")
from django.core.management import execute_from_command_line
import django
from django.conf import settings  # 今回使わないかも一応import
django.setup()
from qiita.models import Article, AccessToken

import mistune   # MarkdownからHTML変換
from qiita_v2.client import QiitaClient


tagger = MeCab.Tagger("-Owakati")


def analysis_user_article():

    article = Article.objects.all()
    print(article[0].article_title, article[0].article_body)


print(analysis_user_article())