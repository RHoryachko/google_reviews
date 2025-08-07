from django.urls import path
from apps.google_reviews.views import GoogleReviewListView, GoogleReviewStatisticsListView


urlpatterns = [
    path("reviews/", GoogleReviewListView.as_view(), name="google_reviews"),
    # path("reviews/statistics/", GoogleReviewStatisticsListView.as_view(), name="google_reviews_statistics"),
]