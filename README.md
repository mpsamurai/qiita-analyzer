# qiita-analyzer
Qiita の記事を分析するモジュール

# import MeCab
sudo apt-get install mecab libmecab-dev mecab-ipadic
sudo aptitude install mecab-ipadic-utf8
sudo apt-get install python-mecab

# pip
sudo apt-get install python3-pip
sudo pip3 install django
sudo pip3 install mistune
sudo pip3 install qiita_v2

# (ubuntu)/home/ubuntu/crontab -e  以下記載
# python3パス
PATH=/usr/bin/python3:/usr/bin:/bin
# djangoのパス
DJANGO_QIITA_ANALYZER=/vagrant/django-qiita-analyzer/mps_apis

# 毎日9時00分に実行(日本時間が-9時間なので)
0 0 * * * python3 /vagrant/qiita-analyzer/qiita-analyzer/article_collection.py >/vagrant/qiita-analyzer/qiita-analyzer/cron_log/logfile 2>&1

# crontabの環境変数を調べる
# * * * * * env >/tmp/cron_env

