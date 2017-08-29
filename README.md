# qiita-analyzer
Qiita article analysis module

# import MeCab
sudo apt-get install mecab libmecab-dev mecab-ipadic
sudo aptitude install mecab-ipadic-utf8
sudo apt-get install python-mecab

## pip install
$ sudo apt-get install python3-pip
$ pip install -r requirements.txt 

## Environmental setting
$ vagrant up  
$ virtualenv venv  
$ source venv/bin/activate  


# Periodic execution crontab
#### python3 PATH_setting
$ (ubuntu)/home/ubuntu/crontab -e  
 
PATH=/usr/bin/python3:/usr/bin:/bin
#### django PATH_setting
$ crontab -e  

DJANGO_QIITA_ANALYZER=/vagrant/django-qiita-analyzer/mps_apis

# article_collection.py Execution

### To the environment of virtualenv

(crontab virtualenv.sh Execution)  
\* * * * * . /vagrant/qiita-analyzer/virtualenv.sh >/vagrant/qiita-analyzer/qiita-analyzer/cron_log/logfile 2>&1



# (Supplement)crontab Environment variable
$ crontab -e  
\* * * * * env >/tmp/cron_env

