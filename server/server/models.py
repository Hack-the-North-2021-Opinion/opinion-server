from django.db import models
import uuid

# models.py: define tables in here

class SearchTerms(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250, unique=True)
    sentiment_score_v1 = models.DecimalField(max_digits=4, decimal_places=3)
    last_updated = models.DateTimeField(auto_now=True)

class SocialMediaPosts(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    content = models.CharField(max_length=1000)
    sentiment = models.DecimalField(max_digits=4, decimal_places=3)
    magnitude = models.DecimalField(max_digits=5, decimal_places=3)
    platform = models.CharField(max_length=250)
    # ForeignKey?
    search_term = models.CharField(max_length=250, unique=True)
