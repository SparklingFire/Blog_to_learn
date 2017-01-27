from articles.models import Article
from comments.models import Comment
from django.db.models.signals import (post_save)
from django.dispatch import receiver
from .models import (RatingModel, Vote)
from django.core.exceptions import ObjectDoesNotExist


@receiver(post_save, sender=Article)
@receiver(post_save, sender=Comment)
def create_rating_model(sender, instance, **kwargs):
    RatingModel.objects.create(content_object=instance)
