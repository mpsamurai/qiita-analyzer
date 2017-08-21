# 参照：http://qiita.com/petitviolet/items/deda7b66852635264508
# 参照：http://qiita.com/Algebra_nobu/items/abe38a5f1fea4aaf1700
# 参照：http://qiita.com/tag1216/items/7e23630d97293e35ea4c

import mistune   # MarkdownからHTML変換
from qiita_v2.client import QiitaClient

# qiitaの個人用アクセストークン
TOKEN = "4eb33e0057f314d4e8cdcc973a906325a24438fa"

class child_QiitaClient(QiitaClient):
    """
    QiitaClientを継承
    """
    def get_particular_user_article(self, id):
        """
        特定のユーザーの特定のタグに関する記事を取得
        :param id: User_id
        :return: タイトル,url,投稿日,更新日,本文 
        """
        # 特定のユーザーの投稿記事一覧を取得
        res_user = self.list_user_items(id)
        article_list = res_user.to_json()
        try:  # その中でも特定のタグ『Python』で取得
            for article in article_list:
                for tags in article['tags']:
                    if tags['name'] == 'Python':
                        # タイトル取得
                        title = article['title']
                        # print("タイトル：%s" % article['title'])
                # urlを取得
                if article['url']:
                    url = article['url']
                    # print("url：%s" % article['url'])
                # 投稿日
                if article['created_at']:
                    created_at = article['created_at']
                    # print("投稿日：%s" % article['created_at'])
                # 最新更新日
                if article['updated_at']:
                    updated_at = article['updated_at']
                    # print("最新更新日：%s" % article['updated_at'])
                # 本文(Markdownで取得)
                if article['body']:
                    # html_body = mistune.markdown(article['body'])
                    article_body = article['body']
                    # print("本文：%s" % article['body'])  # Markdownを取得

                return title, url, created_at, updated_at, article_body
        except KeyError:
            pass


if __name__ == '__main__':
    client = child_QiitaClient(access_token=TOKEN)
    print(client.get_particular_user_article('JunyaKaneko'))