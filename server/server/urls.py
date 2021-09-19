from django.contrib import admin
from django.urls import path

from .views import SearchTermsView, PingView, SocialMediaPostsView

# URLs / Endpoints

urlpatterns = [
    path('admin/', admin.site.urls),

    path('ping/', PingView.as_view()),

    # Endpoints for searchTerms URL.
    path('searchTerms/', SearchTermsView.as_view(), name='searchTerms'),
    path('searchTerms/<str:name>/', SearchTermsView.as_view(), name='searchTerms'),

    # Endpoints for socialMediaPosts URL.
    path('socialMediaPosts/', SocialMediaPostsView.as_view(), name='socialMediaPosts'),
    path('socialMediaPosts/<str:search_term>/', SocialMediaPostsView.as_view(), name='socialMediaPosts'),

    # path('order/', OrdersView.as_view(), name='order'),
]
