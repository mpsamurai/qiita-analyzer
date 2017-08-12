from django.db import models


class Article(models.Model):
    """
    Qiitaの記事を格納するクラス
    """
    title        = models.CharField(max_length=50)
    url          = models.URLField(default=None, blank=True , null=True)
    # created_at   = models.DateTimeField(auto_now=False, auto_now_add=False)
    # updated_at   = models.DateTimeField(auto_now=False, auto_now_add=False)
    article_body = models.TextField(max_length=1000000)

    def __str__(self):
        return self.title