import logging

from django.core.management import call_command
from django.utils.timezone import now
from apps.google_reviews.models import TaskExecution

logging.basicConfig(
    filename="logfile.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

class DailyGoogleReviewsMiddleware:
    """
    Middleware для виклику Django management команди для отримання відгуків з гугла раз в день
    Виконується при кожному запиті, але перевіряє чи минув день з останнього оновлення
    """

    def __init__(self, get_response):
        self.get_response = get_response
        print("DailyGoogleReviewsMiddleware ініціалізовано")

    def __call__(self, request):
        print(f"Middleware викликано для URL: {request.path}")
        self.check_and_run_daily_task()
        
        response = self.get_response(request)
        return response

    def check_and_run_daily_task(self):
        print("Перевіряємо чи потрібно оновити відгуки (раз в день)")
        task_name = "daily_google_reviews_update"
        
        try:
            task, created = TaskExecution.objects.get_or_create(task_name=task_name)
            print(f"TaskExecution: created={created}, last_executed={task.last_executed}")
        except Exception as e:
            print(f"Помилка при створенні/отриманні TaskExecution: {e}")
            return
            
        current_date = now().date()
        print(f"Поточна дата: {current_date}")

        # Перевіряємо чи минув день з останнього оновлення
        if task.last_executed is None or task.last_executed != current_date:
            print(f"Щоденне оновлення ще не виконувалось сьогодні, виконуємо...")
            try:
                logger.info(f"Починаємо щоденне оновлення Google відгуків")
                print(f"Викликаємо команду: daily_google_reviews_update")
                call_command('daily_google_reviews_update')
                
                print(f"Щоденне оновлення відгуків виконано успішно.")
                logger.info(f"Щоденне оновлення відгуків виконано успішно.")
            except Exception as e:
                print(f"Помилка виконання щоденного оновлення: {e}")
                logger.error(f"Помилка виконання щоденного оновлення: {e}")
        else:
            print(f"Щоденне оновлення вже виконувалось сьогодні ({task.last_executed})")