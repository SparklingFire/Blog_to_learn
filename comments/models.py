from django.db import models
from django.conf import settings
from articles.models import Article
from rating.models import RatingModel
from django.contrib.contenttypes.fields import GenericRelation


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, editable=False)
    session = models.CharField(max_length=40, editable=False)
    ip = models.CharField(max_length=40, editable=False)
    parent = models.ForeignKey('self', blank=True, null=True)
    name = models.TextField(editable=False)
    rating_object = GenericRelation(RatingModel)

    def get_likes(self):
        return self.rating_object.last().likes

    def get_dislikes(self):
        return self.rating_object.last().dislikes

    def get_rating_model_pk(self):
        return self.rating_object.last().pk

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.name = '#' + str(self.id)
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Comment ID: {0}'.format(self.id)
