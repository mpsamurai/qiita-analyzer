# 参照：http://qiita.com/petitviolet/items/deda7b66852635264508
# 参照：http://qiita.com/Algebra_nobu/items/abe38a5f1fea4aaf1700
# 参照：http://qiita.com/tag1216/items/7e23630d97293e35ea4c


#### 特定のuserを取得する(自分のidを取得) ####
from qiita_v2.client import QiitaClient
# qiitaの個人用アクセストークン
TOKEN = "4eb33e0057f314d4e8cdcc973a906325a24438fa"

client = QiitaClient(access_token=TOKEN)
# user情報
res_user = client.get_user('hiropon4000')
print(res_user.to_json())

#### 特定の記事へのコメントを返す ###
res_comment = client.list_item_comments('60189aee780feed921a5')
print(res_comment.to_json())