from django.shortcuts import reverse, HttpResponseRedirect, Http404, get_object_or_404
from django.views import generic
from .models import (Article, Subscription)
from django.db.models import Q
from tag.models import Tag
from hit import models as hit_models
from django.core.exceptions import ObjectDoesNotExist
from rating.models import RatingModel
from comments.forms import CommentForm
from comments.models import Comment
from utils_tags_cp.utils import get_ip
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import pytz


class ArticlesList(generic.ListView):
    template_name = 'main_page/article_list.html'
    paginate_by = 5
    search_list = Article.objects.all().order_by('-created')
    tag = None

    def get_queryset(self):
        """
        returns queryset that depends on the Article fields
        """
        if self.tag:
            try:
                return Tag.get_articles_by_tag(self.tag)
            except ObjectDoesNotExist:
                raise Http404
        return self.search_list

    def dispatch(self, request, *args, **kwargs):
        """
        Check if the request is a form request or is a tag request. Fill the target field
        """

        if 'q' in request.GET:
            self.search_list = Article.objects.filter(Q(title__contains=request.GET['q']) |
                                                      Q(text__contains=request.GET['q'])
                                                      )
        if 'tag' in kwargs:
            self.tag = kwargs['tag']

        return super().dispatch(request, *args, **kwargs)


class ArticleDetails(generic.FormView):
    template_name = 'main_page/article_details.html'
    article = None
    form_class = CommentForm

    def get_success_url(self):
        return reverse('article-details', args=[self.article.primary_key])

    def get_context_data(self, **kwargs):
        ctx = super(ArticleDetails, self).get_context_data(**kwargs)
        ctx['article'] = self.article
        ctx['comments'] = self.article.comment_set.all()
        try:
            ctx['subscription'] = Subscription.objects.get(article=self.article,
                                                           session=self.request.session.session_key)
        except ObjectDoesNotExist:
            pass
        return ctx

    def form_valid(self, form):
        comment = form.save(commit=False)
        parent = form['parent'].value()
        if parent:
            comment.parent = Comment.objects.get(pk=int(parent))
        comment.article = self.article
        comment.session = self.request.session.session_key
        comment.ip = get_ip(self.request)
        comment.save()

        subscription_list = Subscription.objects.filter(article=self.article)
        for sub in subscription_list:
            sub.new_comments += 1
            sub.total_comments += 1
            sub.save()

        if self.request.is_ajax():
            data = {'rating_model_pk': comment.get_rating_model_pk(),
                    'comment_text': comment.text,
                    'comment_name': comment.name,
                    'datetime': timezone.now(),
                    'auth_user': False,
                    'comment_pk': comment.id
                    }

            if self.request.user.is_authenticated():
                data.update({'auth_user': True})

            return JsonResponse(data)
        response = super().form_valid(form)
        return response

    def dispatch(self, request, *args, **kwargs):

        try:
            self.article = Article.objects.get(pk=kwargs['pk'])
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('gag'))
        """
        Checks if the model has a hitctcount model and a rating model.
        Adds a hit to an existing hitcount model for that article
        """

        try:
            hit_count_model = self.article.hitcount
        except AttributeError:
            hit_count_model = hit_models.HitCount.objects.create(article=self.article)

        if not self.article.rating_object.last():
            RatingModel.objects.create(content_object=self.article)

        if not request.session.exists(request.session.session_key):
            request.session.create()

        hit_models.Hit.objects.get_or_create(session=request.session.session_key,
                                             hitcount=hit_count_model,
                                             ip=get_ip(self.request))

        try:
            subscription = Subscription.objects.get(article=self.article, session=self.request.session.session_key)
            subscription.new_comments = 0
            subscription.checked_comments = subscription.total_comments
            subscription.save()
        except ObjectDoesNotExist:
            pass

        return super().dispatch(request, *args, **kwargs)


class SiteInfo(generic.TemplateView):
    template_name = 'main_page/static_templates/site_info.html'


class Contacts(generic.TemplateView):
    template_name = 'main_page/static_templates/contacts.html'


class ErrorGag(generic.TemplateView):
    template_name = 'main_page/static_templates/gag.html'


class SubscriptionManagement(generic.RedirectView):
    article = None

    def get_redirect_url(self, *args, **kwargs):
        return self.article.get_absolute_url()

    def dispatch(self, request, *args, **kwargs):
        data = {}
        self.article = get_object_or_404(Article, primary_key=kwargs['primary_key'])
        try:
            sub = Subscription.objects.get(session=request.session.session_key,
                                           ip=get_ip(request),
                                           article=self.article)
            data.update({'sub_id': sub.pk})
            sub.delete()
            data.update({'message': 'Подписаться',
                         'sub_counter': Subscription.objects.filter(session=request.session.session_key).count()})

        except ObjectDoesNotExist:
            sub = Subscription.objects.create(session=request.session.session_key,
                                              ip=get_ip(request),
                                              article=self.article)
            data.update({'sub_id': sub.pk,
                         'message': 'Отписаться',
                         'article': self.article.title,
                         'sub_counter': Subscription.objects.filter(session=request.session.session_key).count()})

        if self.request.is_ajax():
            return JsonResponse(data)

        return super().dispatch(request, *args, **kwargs)


class SubscriptionRefresher(generic.RedirectView):
    pass


@login_required
def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    url = comment.article.get_absolute_url()
    comment.delete()
    if request.is_ajax():
        return JsonResponse({})
    return HttpResponseRedirect(url)


def delete_subscription(request, pk):
    subscription = Subscription.objects.get(pk=pk)
    data = {'pk': subscription.article.primary_key,
            'message': 'Подписаться',
            }
    subscription.delete()
    data.update({'sub_counter': Subscription.objects.filter(session=request.session.session_key).count()})

    if request.is_ajax():
        return JsonResponse(data)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
