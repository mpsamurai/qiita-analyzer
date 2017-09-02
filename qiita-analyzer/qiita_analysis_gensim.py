# -*- coding: utf-8 -*-
import os, sys
import MeCab
from janome.tokenizer import Tokenizer
from gensim import corpora, matutils

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
djangoモデルにあるデータのタイトルを特徴ベクトルにする
"""
mecab = MeCab.Tagger('mecabrc')
t = Tokenizer()
results = []

def word_segmentation(items):
    """タイトルを品詞の単語に分ける"""
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
        if len(r) > 0:
            results.append(r)
        # rl = (" ".join(r).strip())
        # if rl != '':  # 半角空白を取り除く
        #     results.append(rl)
    # print(results)
    return results
    # モデルファイルへ書き出す
    # wakachigaki_file = 'gensim.wakachi'
    # with open(wakachigaki_file, 'w', encoding='utf-8') as fp:
    #     fp.write('\n'.join(results))
def consolidation(results):
    """
    リストの[],[],[]塊をひつとに集約する
    ['x','y',.....]
    """
    results_list = []
    for r in results:
        results_list.append(" ".join(r).strip())
    print(results_list)
    return results_list

if __name__ == '__main__':
    items = ImageRecognitionArticle.objects.all()
    # wordsの単語リストを作る
    words = word_segmentation(items)

    # words(単語リスト[[],[],...))を使って辞書を作る
    dictionary = corpora.Dictionary(words)
    # print(dictionary.token2id)  # idを付ける

    # (テスト)辞書へ特徴語が何個含まれているかを特徴語辞書作る(ID付ける)
    # 先ほど作った辞書と同じ単語リストを使っている
    results_list = consolidation(words)
    tmp = dictionary.doc2bow(results_list)
    # print(tmp)
    # [(0, 1), (1, 1), (2, 1), (3, 1), (4, 3), (5, 1), (6, 1), (7, 1),
    # (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1),
    # (15, 1), (16, 1), (17, 1), (18, 1), (19, 6), (20, 1), (21, 2),
    # (22, 3), (23, 1), (24, 2), (25, 1), (26, 2), (27, 1), (28, 1), (29, 3),
    # (30, 1), (31, 1), (32, 1), (33, 2), (34, 1), (35, 1), (36, 1), (37, 1),
    # (38, 1), (39, 1), (40, 1), (41, 4), (42, 1), (43, 1), (44, 1), (45, 1),
    # (46, 1), (47, 1), (48, 2), (49, 1), (50, 1), (51, 1), (52, 1), (53, 1),
    # (54, 1), (55, 1), (56, 1), (57, 1), (58, 1), (59, 1), (60, 1), (61, 1),
    # (62, 1), (63, 1), (64, 1), (65, 1), (66, 1), (67, 1), (68, 1), (69, 1)]

  # 辞書ID(tmp)が作られたのでそれを特徴ベクトルにする
    dense = list(matutils.corpus2dense([tmp], num_terms=len(dictionary)).T[0])
    # print(dense)
    # [1.0, 1.0, 1.0, 1.0, 3.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
    #  1.0, 1.0, 1.0, 1.0, 1.0, 6.0, 1.0, 2.0, 3.0, 1.0, 2.0, 1.0, 2.0, 1.0, 1.0,
    #  3.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 4.0, 1.0, 1.0,
    #  1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
    #  1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]



