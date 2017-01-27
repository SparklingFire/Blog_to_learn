from django.shortcuts import redirect, HttpResponseRedirect
from .models import (Vote, RatingModel)
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from utils_tags_cp.utils import get_ip


def rating_view(request, pk, vote):

    like = True if vote == 'like' else False

    try:
        rating_model = RatingModel.objects.get(pk=pk)
    except ObjectDoesNotExist:
        redirect('gag')

    """
       The view tries to get a vote object with existing parameters. If it's found, the object is going to be
       deleted or changed. If not, just create one more Vote object.
    """

    try:
        vote = Vote.objects.get(session=request.session.session_key,
                                ip=get_ip(request),
                                rating_model=rating_model)
        if vote.like == like:
            vote.delete()
        else:
            vote.like = like
            vote.save()

    except ObjectDoesNotExist:
        Vote.objects.create(session=request.session.session_key,
                            ip=get_ip(request),
                            like=like,
                            rating_model=rating_model)

    rating_model.calculate_score()
    if request.is_ajax():
        return JsonResponse({'likes': str(rating_model.likes),
                             'dislikes': str(rating_model.dislikes)})

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
