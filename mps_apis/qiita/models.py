from django.db import models


class Article(models.Model):
    """
    Qiitaの記事を格納するクラス
    """
    title        = models.CharField(max_length=50)
    url          = models.URLField()
    created_at   = models.DateTimeField(auto_now=False, auto_now_add=False)
    updated_at   = models.DateTimeField(auto_now=False, auto_now_add=False)
    article_body = models.TimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.title