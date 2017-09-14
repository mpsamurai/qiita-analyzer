# Description
### This module uses Qiita_API to acquire specific articles.

# pip install
>$ sudo apt-get install python3-pip 


# git clone and setup.py install
>$ cd sample_project  
$ git clone git@github.com:aporo4000/django-qiita-analyzer.git  
$ cd django-qiita-analyzer  
$ pip install -r requirements.txt   
$ python setup.py install   

 Finished!  

git clone git@github.com:aporo4000/qiita-analyzer.git

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
$ (ubuntu)/home/ubuntu/crontab -e    

DJANGO_QIITA_ANALYZER=/vagrant/django-qiita-analyzer/mps_apis

#### client_id, client_secret PATH_setting
$ (ubuntu)/home/ubuntu/crontab -e    

export CLIENT_ID="1c1acbb548947cbbe46b4f0ccc4c87460d3f0628"
export CLIENT_SECRET="995436fc01b1637eb45907123d9ea282f7bb400b"


# article_collection.py Execution

### To the environment of virtualenv
$ (ubuntu)/home/ubuntu/crontab -e   

\# (crontab virtualenv.sh Execution)  
\* * * * * . /vagrant/qiita-analyzer/qiita_analyzer/virtualenv.sh >/vagrant/qiita-analyzer/qiita_analyzer/cron_log/logfile 2>&1



# (Supplement)crontab Environment variable
$ (ubuntu)/home/ubuntu/crontab -e  
\* * * * * env >/tmp/cron_env

