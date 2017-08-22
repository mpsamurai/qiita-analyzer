# django-qiita-analyzerモジュールをimportしてdjangoモデル使う
# localファイル.bash_profile
# MPSのdjango-qiita-analyzerパス
# export DJANGO_QIITA_ANALYZER=/Users/hiroshiteraoka/MPS/mps_website/django-qiita-analyzer/mps_apis

import os, sys
import MeCab
from gensim import corpora, models, similarities

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
title_documents = []

def analysis_test_article():

    article = Article.objects.all()
    for item in article:
        title_documents.extend(tagger.parse(item.article_title).split(' '))
        # title_documents.append(item.article_title)
    # print(title_documents)


    stoplist = set('の ため た - / 2 を ( ) から ; : \n , .'.split())  # 除外するリスト
    # print(stoplist)

    texts = [[word for word in document.split() if word not in stoplist]
             for document in title_documents]
    print(texts)
    all_tokens = sum(texts, [])
    tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    print(tokens_once)
    text_list = [[word for word in text if word not in tokens_once]
             for text in texts]


    print(text_list)




# analysis_test_article()