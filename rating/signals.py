from articles.models import Article
from comments.models import Comment
from django.db.models.signals import (post_save, pre_delete)
from django.dispatch import receiver
from .models import (RatingModel, Vote)
from django.core.exceptions import ObjectDoesNotExist
from custom_user.models import CustomUser
from .models import (UserRatingModel, RatingModel)
from django.db import (transaction, IntegrityError)


@receiver(post_save, sender=Article)
@receiver(post_save, sender=Comment)
def create_rating_model(sender, instance, **kwargs):
    if instance.author:
        RatingModel.objects.create(content_object=instance,
                                   user_rating_model=instance.author.userratingmodel)
    else:
        RatingModel.objects.create(content_object=instance)


@receiver(post_save, sender=RatingModel)
@receiver(pre_delete, sender=Vote)
@receiver(pre_delete, sender=Article)
@receiver(pre_delete, sender=Comment)
def update_user_rating(sender, instance, **kwargs):
    try:
        if sender in (Article, Comment):
            instance.get_rating_model().user_rating_model.calculate_score()
        elif sender == Vote:
            instance.rating_model.user_rating_model.calculate_score()
        else:
            instance.user_rating_model.calculate_score()
    except ObjectDoesNotExist:
        pass


@receiver(post_save, sender=CustomUser)
def create_user_rating_model(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            UserRatingModel.objects.create(user=instance)
    except IntegrityError:
        pass
