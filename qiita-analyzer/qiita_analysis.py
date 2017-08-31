import os, sys

# このファイル実行前に一度上記exportをコマンドラインでパス通す
django_qiita_analyzer = os.environ['DJANGO_QIITA_ANALYZER']
sys.path.append(django_qiita_analyzer)  # django-qiita-analyzerへパス通す
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mps_apis.settings")
from django.core.management import execute_from_command_line
import django
from django.conf import settings
django.setup()
from django_qiita_analyzer.models import MachineLearningArticle, \
    NLPArticle, ImageRecognitionArticle, DepthLearningArticle

from janome.tokenizer import Tokenizer
t = Tokenizer()
# 単語の出現頻度をカウントする
# 単語の辞書を作成
worddic = {}
items = ImageRecognitionArticle.objects.all()
for item in items:
    malist = t.tokenize(item.article_title)  # 一行一行形態素解析
    for w in malist:
        word = w.surface
        part = w.part_of_speech
        if part.find('名詞') < 0:
            continue
        if not word in worddic:
            worddic[word] = 0
        worddic[word] += 1

keys = sorted(worddic.items(), key=lambda x: x[1], reverse=True)
for word, cnt in keys[:50]:
    print("{0}({1})\n".format(word, cnt), end="")
    # タイトルでよく出てくる単語を分解すると以下の様な状況
"""
画像(43)
認識(29)
-(24)
OpenCV(20)
)(14)
((14)
Python(12)
.(10)
顔(9)
Visual(9)
Recognition(9)
API(9)
検出(8)
論文(8)
調査(7)
:(6)
カメラ(6)
](6)
ため(6)
学習(6)
推定(6)
2(6)
～(6)
Vision(6)
[(6)
アプリ(6)
化(6)
1(6)
GPU(5)
初心者(5)
Watson(5)
Tutorials(5)
処理(5)
Microsoft(5)
コード(5)
3(5)
CNN(4)
image(4)
動画(4)
実装(4)
ディープラーニング(4)
データ(4)
Networks(4)
Scikit(4)
内容(4)
上(4)
中(4)
文字(4)
言語(4)
物体(4)
"""