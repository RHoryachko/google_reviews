from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import GoogleReview, GoogleReviewStatistics
from .serializers import GoogleReviewSerializer, GoogleReviewStatisticsSerializer


@extend_schema_view(
    get=extend_schema(
        summary="List all Google reviews",
        description="Retrieve all Google reviews for the company",
        tags=["Google Reviews"],
    )
)
class GoogleReviewListView(ListAPIView):
    queryset = GoogleReview.objects.all()
    serializer_class = GoogleReviewSerializer
    pagination_class = None


@extend_schema_view(
    get=extend_schema(
        summary="Get Google review statistics",
        description="Retrieve Google review statistics and metrics",
        tags=["Google Reviews"],
    )
)
class GoogleReviewStatisticsListView(ListAPIView):
    queryset = GoogleReviewStatistics.objects.all()
    serializer_class = GoogleReviewStatisticsSerializer
    pagination_class = None