from django.db import models


class AccessToken(models.Model):

    token = models.CharField(max_length=50)

    def __str__(self):
        return self.token

class Article(models.Model):
    """
    Qiitaの記事を格納するクラス
    """
    article_title        = models.CharField(max_length=50, default=None, blank=True, null=True)
    url          = models.URLField(default=None, blank=True, null=True)
    # created_at   = models.DateTimeField(auto_now=False, auto_now_add=False)
    # updated_at   = models.DateTimeField(auto_now=False, auto_now_add=False)
    article_body = models.TextField(max_length=100000)
    article_token = models.ForeignKey(AccessToken, default=None, blank=True, null=True, related_name='article_token')

    def __str__(self):
        return self.article_title