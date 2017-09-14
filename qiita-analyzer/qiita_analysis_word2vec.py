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
from gensim.models import word2vec
import re
"""
djangoモデルにある”画像認識”データのタイトルだけ全て取得して
その語句の頻出量を出して、与えられた単語ににている単語をだす
"""

t = Tokenizer()
results = []

items = ImageRecognitionArticle.objects.all()
for item in items:
    s = item.article_title  # 各タイトルへ処理する
    s = s.split('\r\n')  # タイトルごとに分ける
    s = re.sub('[【】\[\] \- \' 、。「」（）()『』～ ~ ？]', '', str(s))  # 不要な記号除去
    tokens = t.tokenize(s)  # トークナイザーを使ってタイトルを分解
    r = []
    for token in tokens:  # それぞれを処理
        if token.base_form == '*':  # 品詞が基本形なら
            w = token.surface
        else:
            w = token.base_form  # 違うなら活用前を利用
    ps = token.part_of_speech  # トークナイザーの変数
    hinshi = ps.split(',')[0]
    if hinshi in ['名詞', '形容詞', '動詞', '記号']:
        r.append(w)
    rl = (" ".join(r).strip())
    results.append(rl)
    # モデルファイルへ書き出す
    wakachigaki_file = 'qiita.wakachi'
    with open(wakachigaki_file, 'w', encoding='utf-8') as fp:
        fp.write('\n'.join(results))

# モデルを作る
data = word2vec.LineSentence(wakachigaki_file)
model = word2vec.Word2Vec(data, size=200, window=10, hs=1, min_count=2, sg=1)
model.save('qiita.model')
print('Completed')

# モデルを使う
print(model.most_similar(positive=['認識']))