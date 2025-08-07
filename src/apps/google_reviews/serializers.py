from rest_framework import serializers
from apps.google_reviews.models import GoogleReview, GoogleReviewStatistics


class GoogleReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleReview
        fields = ["id", "name", "href",
                  "avatar_url", "text", "rating", 
                  "date", "profile_url"]
        

class GoogleReviewStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleReviewStatistics
        fields = ["id", "date", "total_reviews", "total_rating", "average_rating"]