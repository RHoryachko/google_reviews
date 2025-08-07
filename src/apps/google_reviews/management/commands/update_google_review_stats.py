from django.core.management.base import BaseCommand
from django.db import models
from apps.google_reviews.models import GoogleReview, GoogleReviewStatistics
from datetime import date
import json
import re

class Command(BaseCommand):
    help = 'Update or create Google Review statistics for today (автоматично або з JSON)'

    def add_arguments(self, parser):
        parser.add_argument('--json', type=str, required=False, help='Raw JSON string from Google Maps')

    def handle(self, *args, **options):
        total_reviews = None
        average_rating = None
        total_rating = None
        raw_json = options.get('json')

        if raw_json:
            try:
                data = json.loads(raw_json)
                # Парсимо кількість відгуків і рейтинг з вкладених масивів
                def extract_reviews_and_rating(data):
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, list):
                                for subitem in item:
                                    if isinstance(subitem, list):
                                        for subsubitem in subitem:
                                            if isinstance(subsubitem, list):
                                                for el in subsubitem:
                                                    if isinstance(el, str) and "Відгуків" in el:
                                                        match = re.search(r"Відгуків: (\d+)", el)
                                                        if match:
                                                            total_reviews = int(match.group(1))
                                                            idx = subsubitem.index(el)
                                                            for offset in range(1, 4):
                                                                if idx - offset >= 0 and isinstance(subsubitem[idx - offset], (int, float)):
                                                                    average_rating = subsubitem[idx - offset]
                                                                    return total_reviews, average_rating
                    return None, None
                total_reviews, average_rating = extract_reviews_and_rating(data)
                if total_reviews is None or average_rating is None:
                    self.stdout.write(self.style.ERROR('Could not parse total_reviews or average_rating from JSON.'))
                    return
                total_rating = int(total_reviews * average_rating)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error parsing JSON: {e}'))
                return
        else:
            total_reviews = GoogleReview.objects.count()
            average_rating = GoogleReview.objects.aggregate(avg=models.Avg('rating'))['avg'] or 0
            total_rating = GoogleReview.objects.aggregate(total=models.Sum('rating'))['total'] or 0

        obj, created = GoogleReviewStatistics.objects.update_or_create(
            date=date.today(),
            defaults={
                'total_reviews': total_reviews,
                'average_rating': average_rating,
                'total_rating': total_rating,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created new statistics record for today.'))
        else:
            self.stdout.write(self.style.SUCCESS('Updated statistics record for today.'))