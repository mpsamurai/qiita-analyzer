# django-qiita-analyzerモジュールをimportしてdjangoモデル使う
# localファイル.bash_profile
# MPSのdjango-django_qiita_analyzer-analyzerパス
# export DJANGO_QIITA_ANALYZER=/Users/hiroshiteraoka/MPS/mps_website/django-django_qiita_analyzer-analyzer/mps_apis

import os, sys

# このファイル実行前に一度上記exportをコマンドラインでパス通す
django_qiita_analyzer = os.environ['DJANGO_QIITA_ANALYZER']
sys.path.append(django_qiita_analyzer)  # django-qiita-analyzerへパス通す
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mps_apis.settings")
from django.core.management import execute_from_command_line
import django
from django.conf import settings
django.setup()
# from django_qiita_analyzer.models import Article, AllArticle, AccessToken
from django_qiita_analyzer.models import Article, AccessToken
import django_qiita_analyzer.credentials as credentials

import mistune   # MarkdownからHTML変換
from qiita_v2.client import QiitaClient
import qiita_all_articles_collection as qiita2


class ParticularUserArticle():
    """
    特定のUserの記事について
    """
    def __init__(self):
        # django_qiita_analyzerモデルから最新のTOKENを取得
        TOKEN = AccessToken.latest_token.get_latest_token()
        print("TOKEN", TOKEN)
        if TOKEN == None:
            print("AccessTokenがない")
        else:
            self.client = QiitaClient(access_token=TOKEN)
            self.id = credentials.id
            self.tag = credentials.tag
            print("idとtag", self.id, self.tag)


    def get_particular_user_tag_article(self):
        """
        特定のユーザーの特定のタグに関する記事を取得
        update_or_createで重複保存を無くし、更新されたら保存 
        """
        # 特定のユーザーの投稿記事一覧を取得
        try:
            res_user = self.client.list_user_items(self.id)
            article_list = res_user.to_json()
            # その中でも特定のタグ『Python』で取得
            for article in article_list:
                for tags in article['tags']:
                    if tags['name'] == self.tag:
                        # タイトル取得
                        title = article['title']
                        print(title)
                # urlを取得
                if article['url']:
                    url = article['url']
                # 投稿日
                if article['created_at']:
                    created_at = article['created_at']
                # 最新更新日
                if article['updated_at']:
                    updated_at = article['updated_at']
                # 本文(Markdownで取得)
                if article['body']:
                    article_body = article['body']

                    # update_or_createで重複保存を無くし、更新されたら保存
                    Article.objects.update_or_create(article_title=title,
                                                     url=url,
                                                     created_at=created_at,
                                                     updated_at=updated_at,
                                                     article_body=article_body)


        except AttributeError:
            print("AccessTokenがないよ")

if __name__ == '__main__':
    particular_user = ParticularUserArticle()
    particular_user.get_particular_user_tag_article()


# def get_all_tag_articles(tag):
#     """
#     qiita_all_articles_collectionファイル参照
#     :param tag: "Python"
#     djangoモデルへ保存
#     """
#     qiita2.wait_seconds = 0
#     for item in qiita2.tag_items(tag, 100, 5):  # qiita2.tag_items(tag_url, per_page, max_page)
#         AllArticle.objects.create(article_title=item["title"],
#                                   url=item["url"],
#                                   created_at=item["created_at"],
#                                   updated_at=item["updated_at"],
#                                   article_body=item["rendered_body"])
#         # print(item["title"])
#         # qiita2.save_item(item)
#
# get_all_tag_articles(tag)