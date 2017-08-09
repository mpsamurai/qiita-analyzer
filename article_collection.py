# 参照：http://qiita.com/petitviolet/items/deda7b66852635264508
# 参照：http://qiita.com/Algebra_nobu/items/abe38a5f1fea4aaf1700
# 参照：http://qiita.com/tag1216/items/7e23630d97293e35ea4c


from qiita_v2.client import QiitaClient
# qiitaの個人用アクセストークン
TOKEN = "4eb33e0057f314d4e8cdcc973a906325a24438fa"

def get_particular_article(id):
    client = QiitaClient(access_token=TOKEN)
    # 特定のユーザーの投稿記事一覧を取得
    res_user = client.list_user_items(id)
    article_list = res_user.to_json()
    for article in article_list:
        for tags in article['tags']:
            if tags['name'] == 'QiitaAPI':
                print(article['title'])


get_particular_article('hiropon4000')