from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.db import Error, IntegrityError
from django.db.transaction import atomic
from psycopg2 import errorcodes
import json
import sys
import time
import datetime

from .models import *

# views.py: Read and write transaction operations on tables defined in models.py

# Warning: Do not use retry_on_exception in an inner nested transaction.

def retry_on_exception(num_retries=3, on_failure=HttpResponse(status=500), delay_=0.5, backoff_=1.5):
    def retry(view):
        def wrapper(*args, **kwargs):
            delay = delay_
            for i in range(num_retries):
                try:
                    return view(*args, **kwargs)
                except IntegrityError as ex:
                    if i == num_retries - 1:
                        return on_failure
                    elif getattr(ex.__cause__, 'pgcode', '') == errorcodes.SERIALIZATION_FAILURE:
                        time.sleep(delay)
                        delay *= backoff_
                except Error as ex:
                    return on_failure
        return wrapper
    return retry


class PingView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("python/django", status=200)


@method_decorator(csrf_exempt, name='dispatch')
class SearchTermsView(View):
    def get(self, request, name=None, *args, **kwargs):
        if name is None:
            searchTerms = list(SearchTerms.objects.values())
        else:
            searchTerms = list(SearchTerms.objects.filter(name=name).values())[0]
        return JsonResponse(searchTerms, safe=False)

    @retry_on_exception(3)
    @atomic
    def post(self, request, *args, **kwargs):
        form_data = json.loads(request.body.decode())
        name = form_data['name']
        sentiment_score_v1 = form_data['sentiment_score_v1']
        c = SearchTerms(
            name=name, 
            sentiment_score_v1=sentiment_score_v1,
            last_updated=datetime.datetime.now()
        )
        c.save()
        return HttpResponse(status=200)

    @retry_on_exception(3)
    @atomic
    def delete(self, request, id=None, *args, **kwargs):
        if id is None:
            return HttpResponse(status=404)
        SearchTerms.objects.filter(id=id).delete()
        return HttpResponse(status=200)

    @retry_on_exception(3)
    @atomic
    def patch(self, request, name=None, *args, **kwargs):
        form_data = json.loads(request.body.decode())
        if name is None:
            return HttpResponse(status=404)
        sentiment_score_v1 = form_data['sentiment_score_v1']
        c = SearchTerms.objects.get(name=name)
        c.sentiment_score_v1 = sentiment_score_v1
        c.save()
        return HttpResponse(status=200)


@method_decorator(csrf_exempt, name='dispatch')
class SocialMediaPostsView(View):
    def get(self, request, search_term=None, *args, **kwargs):
        if search_term is None:
            # Return at most 30 social media posts
            socialMediaPosts = list(SocialMediaPosts.objects.values())[:30]
        else:
            # Return at most 30 social media posts
            socialMediaPosts = list(SocialMediaPosts.objects.filter(search_term=search_term).values())[:30]
        return JsonResponse(socialMediaPosts, safe=False)

    @retry_on_exception(3)
    @atomic
    # Need to a bulk API for this...
    def post(self, request, *args, **kwargs):
        form_data = json.loads(request.body.decode())
        content = form_data['content']
        sentiment = form_data['sentiment']
        magnitude = form_data['magnitude']
        platform = form_data['platform']
        search_term = form_data['search_term']
        c = SocialMediaPosts(
            content=content, 
            sentiment=sentiment,
            magnitude=magnitude,
            platform=platform,
            search_term=search_term
        )
        c.save()
        return HttpResponse(status=200)

    @retry_on_exception(3)
    @atomic
    def delete(self, request, id=None, *args, **kwargs):
        if id is None:
            return HttpResponse(status=404)
        SocialMediaPosts.objects.filter(id=id).delete()
        return HttpResponse(status=200)

    # @retry_on_exception(3)
    # @atomic
    # def patch(self, request, *args, **kwargs):
    #     form_data = json.loads(request.body.decode())
    #     name = form_data['name']
    #     sentiment_score_v1 = form_data['sentiment_score_v1']
    #     c = SearchTerms.objects.get(name=name) 
    #     c.sentiment_score_v1 = sentiment_score_v1
    #     c.save()
    #     return HttpResponse(status=200)