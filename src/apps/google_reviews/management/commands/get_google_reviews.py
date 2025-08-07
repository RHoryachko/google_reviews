import json
import requests

from django.core.management.base import BaseCommand
from apps.google_reviews.models import GoogleReview

class Command(BaseCommand):
    help = 'Fetch and parse Google reviews from API'

    def handle(self, *args, **options):
        url = "https://www.google.com/maps/rpc/listugcposts?authuser=0&hl=uk&gl=ua&pb=!1m6!1s0x473a4d44bfebb121%3A0xc00b62ac9cc3b494!6m4!4m1!1e1!4m1!1e3!2m2!1i10!2s!5m2!1sZwGRaPT9CPK_wPAP1YfcwAo!7e81!8m9!2b1!3b1!5b1!7b1!12m4!1b1!2b1!4m1!1e1!11m0!13m1!1e1"

        try:
            # Виконуємо запит
            response = requests.get(url)
            response.raise_for_status()
            
            # Обробляємо відповідь
            raw_data = response.text
            if raw_data.startswith(")]}'\n"):
                json_data = raw_data[5:]
            else:
                json_data = raw_data

            data = json.loads(json_data)
            
            # Отримуємо список відгуків
            reviews_list = data[2] if len(data) > 2 else []
            
            for review in reviews_list:
                try:
                    # Основна інформація про відгук
                    review_info = review[0]
                    review_data = review_info[2]
                    translations = review_data[-1]
                    author_info = review_info[1][4][5]
                    name = author_info[0]
                    avatar_url = author_info[1]
                    profile_id = author_info[3]
                    profile_url = f"https://www.google.com/maps/contrib/{profile_id}"
                    date = review_info[1][6]
                    # print("rating------")
                    rating = review_info[2][0][0]
                    # print(rating)


                    # Зберігаємо в базу даних
                    review, created = GoogleReview.objects.update_or_create(
                        name=name,
                        text=translations[0][0],
                        rating=rating,
                        defaults={
                            'date': date,
                            'avatar_url': avatar_url,
                            'profile_url': profile_url
                        }
                    )
                    
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created new review by {name}'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Updated existing review by {name}'))
                    
                except (IndexError, TypeError, KeyError) as e:
                    self.stdout.write(self.style.WARNING(f'Skipping malformed review: {str(e)}'))
                    continue

            self.stdout.write(self.style.SUCCESS(f'Successfully processed {len(reviews_list)} reviews'))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Request failed: {str(e)}'))
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f'Failed to parse JSON: {str(e)}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Unexpected error: {str(e)}'))