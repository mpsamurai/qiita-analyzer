#!/bin/sh

# venvがある場所へ
PROG_DIR=/vagrant/venv

# vietualenv環境へ(本来sourceだけど ubuntuの場合shellから動かないので . で実行)
. $PROG_DIR/bin/activate
# pythonファイル実行
python3 /vagrant/qiita-analyzer/qiita-analyzer/article_collection.py