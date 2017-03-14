from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify
from django.shortcuts import reverse
from django.contrib.contenttypes.fields import GenericRelation
from rating.models import RatingModel


class ArticleManager(models.Manager):
    def get_popular_articles(self):
        return Article.objects.all().order_by('hitcount__hits').reverse()


class Article(models.Model):
    title = models.CharField(max_length=100, unique=True)
    text = models.TextField()
    created = models.DateTimeField(default=timezone.now, editable=False)
    edited = models.DateTimeField(default=timezone.now, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    primary_key = models.SlugField(primary_key=True, unique=True, max_length=100, editable=False)
    rating_object = GenericRelation(RatingModel)

    def save(self, *args, **kwargs):
        """
        create a primary key for the article before saving the object
        """

        self.primary_key = slugify(self.title)
        super().save(*args, **kwargs)

    def get_hits(self):
        return self.hitcount.hits

    def get_likes(self):
        return self.rating_object.last().likes

    def get_dislikes(self):
        return self.rating_object.last().dislikes

    def get_rating_model_pk(self):
        return self.rating_object.last().pk

    def get_rating_model(self):
        return RatingModel.objects.get(pk=self.get_rating_model_pk())

    def get_article_tags(self):
        return self.tag_set.all()

    def get_absolute_url(self):
        return reverse('article-details', args=[str(self.primary_key)])

    objects = ArticleManager()


class Subscription(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    subscribed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    session = models.CharField(max_length=40, editable=False)
    ip = models.CharField(max_length=40, editable=False)
    new_comments = models.SmallIntegerField(default=0)
    checked_comments = models.SmallIntegerField(default=0)
    total_comments = models.SmallIntegerField(default=0)

    def __str__(self):
        return 'The subscription on {0}'.format(self.article.title)
