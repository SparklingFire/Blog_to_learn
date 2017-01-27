from articles.models import (Article, Subscription)
from articles.forms import SearchForm
from tag.models import Tag


def popular_articles(request):
    articles = Article.objects.get_popular_articles()[:5]
    return {'POPULAR_ARTICLES': articles}


def subscriptions(request):
    subscription_list = Subscription.objects.filter(session=request.session.session_key)
    return {"SUBSCRIPTION_LIST": subscription_list}


def tag_list(request):
    tags = Tag.objects.all()
    return {"TAGS": tags}


def search_form(request):
    form = SearchForm
    return {"SEACH_FORM": form}
