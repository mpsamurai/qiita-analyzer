# 参照：http://qiita.com/tag1216/items/7e23630d97293e35ea4c#%E7%89%B9%E5%AE%9A%E3%82%BF%E3%82%B0%E3%81%AE%E6%8A%95%E7%A8%BF%E4%B8%80%E8%A6%A7%E3%81%AE%E5%8F%96%E5%BE%97
# 参照(html -> text変換)：http://nekoyukimmm.hatenablog.com/entry/2015/12/24/113719
from readability.readability import Document
import html2text

import os, sys

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

import time
import codecs
import json
from logging import getLogger
import requests
from urllib.parse import urlparse, parse_qs


logger = getLogger(__name__)

URL_ITEMS     = "https://qiita.com/api/v2/items"
URL_TAG_ITEMS = "https://qiita.com/api/v2/tags/%s/items"
URL_TAGS      = "https://qiita.com/api/v2/tags"

HEADER_TOTAL = "Total-Count"
LINK_NEXT = "next"
LINK_LAST = "last"

default_per_page = 100
default_max_page = 100
wait_seconds = 12
retry_wait_min = 1
retry_limit = 10

auth_token = None

def items(per_page=default_per_page, max_page=default_max_page):
    req = QiitaRequest(URL_ITEMS, per_page, max_page)
    return QiitaIterator(req)

def tag_items(tag_url, per_page=default_per_page, max_page=default_max_page):
    req = QiitaRequest(URL_TAG_ITEMS % tag_url, per_page, max_page)
    return QiitaIterator(req)

def tags(per_page=default_per_page, max_page=default_max_page):
    req = QiitaRequest(URL_TAGS, per_page, max_page)
    return QiitaIterator(req)

class QiitaIterator:
    def __init__(self, req):
        self.req = req
        self.items = req.request().__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        if self.items == None:
            raise StopIteration
        try:
            val = self.items.__next__()
            return val
        except StopIteration:
            if self.req.has_next():
                self.items = self.req.next().__iter__()
                return self.__next__()
            else:
                raise StopIteration

    def __len__(self):
        return self.req.total_count()

class QiitaRequest:

    last_request_time = None

    retry_num = 0

    def __init__(self, url, per_page=default_per_page, max_page=default_max_page, page=1):
        self.url = url
        self.per_page = per_page
        self.max_page = max_page
        self.page = page
        self.res = None
        self.current_page = None

    def request(self):
        self.links = dict()
        params = {"per_page": self.per_page, "page": self.page}
        return self.__request__(self.url, params)

    def __request__(self, url, params=None):
        self.__wait__()
        logger.info("url:%s" % url)

        headers = {"Authorization": "Bearer " + auth_token} if auth_token != None else None
        self.res = requests.get(url, params=params, headers=headers)
        status = self.res.status_code

        while status != 200 and QiitaRequest.retry_num <= retry_limit:
            logger.warning("status:%d" % status)
            logger.warn(u"%d分待機します。" % retry_wait_min)
            time.sleep(retry_wait_min * 60)
            QiitaRequest.retry_num = QiitaRequest.retry_num + 1
            self.res = requests.get(url, params = params)
            status = self.res.status_code

        if status != 200:
            logger.warning("status:%d" % status)
            logger.warning(self.res.text)
            return None

        QiitaRequest.retry_num = 0
        return self.res.json()

    def next(self):
        if not self.has_next():
            raise Exception()
        # v2でLinkレスポンスヘッダでper_pageが欠落している不具合の対応
        params = {"per_page": self.per_page}
        return self.__request__(self.res.links[LINK_NEXT]["url"], params)

    def retry(self):
        pass
    def has_error(self):
        pass
    def has_next(self):
        if not LINK_NEXT in self.res.links: return False
        url = self.res.links[LINK_NEXT]["url"]
        page = self.__get_page__(url)
        return page <= self.max_page

    def last_page(self):
        url = self.res.links[LINK_LAST]["url"]
        return self.__get_page__(url)

    def total_count(self):
        return int(self.res.headers[HEADER_TOTAL])

    def __get_page__(self, url):
        query = urlparse(url).query
        page = parse_qs(query)["page"][0]
        return int(page)

    def __wait__(self):
        if QiitaRequest.last_request_time != None:
            last = QiitaRequest.last_request_time
            now = time.clock()
            wait = wait_seconds - (now - last)
            if 0 < wait:
                time.sleep(wait)
        QiitaRequest.last_request_time = time.clock()

def save_item(model_name, item):
    """update_or_createで重複保存を無くし保存"""
    # html -> textへ変換以下2行
    item_article_body = Document(item['rendered_body']).summary()
    article_body_text = html2text.html2text(item_article_body)

    if model_name == 'MachineLearningArticle':
        MachineLearningArticle.objects.update_or_create(article_title=item['title'],
                                                        url=item['url'],
                                                        created_at=item['created_at'],
                                                        updated_at=item['updated_at'],
                                                        article_body=article_body_text)
    if model_name == 'NLPArticle':
        NLPArticle.objects.update_or_create(article_title=item['title'],
                                            url=item['url'],
                                            created_at=item['created_at'],
                                            updated_at=item['updated_at'],
                                            article_body=article_body_text)

    if model_name == 'ImageRecognitionArticle':
        ImageRecognitionArticle.objects.update_or_create(article_title=item['title'],
                                                         url=item['url'],
                                                         created_at=item['created_at'],
                                                         updated_at=item['updated_at'],
                                                         article_body=article_body_text)

    if model_name == 'DepthLearningArticle':
        DepthLearningArticle.objects.update_or_create(article_title=item['title'],
                                                      url=item['url'],
                                                      created_at=item['created_at'],
                                                      updated_at=item['updated_at'],
                                                      article_body=article_body_text)

if __name__ == '__main__':
    wait_seconds = 0
    for item in tag_items('画像認識', 100, 5):
        save_item('ImageRecognitionArticle', item)
