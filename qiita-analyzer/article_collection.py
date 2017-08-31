# django-qiita-analyzerモジュールをimportしてdjangoモデル使う
# localファイル.bash_profile
# MPSのdjango-django_qiita_analyzer-analyzerパス
# export DJANGO_QIITA_ANALYZER=/vagrant/django-qiita-analyzer/mps_apis

import os, sys

# このファイル実行前に一度上記exportをコマンドラインでパス通す
django_qiita_analyzer = os.environ['DJANGO_QIITA_ANALYZER']
sys.path.append(django_qiita_analyzer)  # django-qiita-analyzerへパス通す
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mps_apis.settings")
from django.core.management import execute_from_command_line
import django
from django.conf import settings

django.setup()

from django_qiita_analyzer.models import OauthArticle, AccessToken
import django_qiita_analyzer.credentials as credentials

import mistune   # MarkdownからHTML変換
from qiita_v2.client import QiitaClient


class ParticularUserArticle():
    """
    特定のUserの記事について
    """
    def __init__(self):
        # django_qiita_analyzerモデルから最新のTOKENを取得
        TOKEN = AccessToken.latest_token.get_latest_token()
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
                    OauthArticle.objects.update_or_create(article_title=title,
                                                          url=url,
                                                          created_at=created_at,
                                                          updated_at=updated_at,
                                                          article_body=article_body)


        except AttributeError:
            print("AccessTokenがないよ")

if __name__ == '__main__':
    particular_user = ParticularUserArticle()
    particular_user.get_particular_user_tag_article()


