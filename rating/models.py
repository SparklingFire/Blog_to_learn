from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class RatingModel(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='tied object')
    object_id = models.SlugField()
    content_object = GenericForeignKey('content_type', 'object_id')

    score = models.SmallIntegerField(default=0)
    likes = models.SmallIntegerField(default=0)
    dislikes = models.SmallIntegerField(default=0)
    created = models.DateTimeField(default=timezone.now, editable=False)
    edited = models.DateTimeField(default=timezone.now, editable=False)

    def get_related_article(self):
        return self.article

    def calculate_score(self):
        self.likes = len(self.vote_set.filter(like=True))
        self.dislikes = len(self.vote_set.filter(like=False))

        self.score = self.likes - self.dislikes
        self.save()


class Vote(models.Model):
    like = models.BooleanField(default=True)
    rating_model = models.ForeignKey(RatingModel, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, editable=False)
    edited = models.DateTimeField(default=timezone.now, editable=False)
    session = models.CharField(max_length=40, editable=False)
    ip = models.CharField(max_length=40, editable=False)
