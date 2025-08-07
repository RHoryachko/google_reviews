from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils.timezone import now
from apps.google_reviews.models import TaskExecution
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Щоденне оновлення Google відгуків та статистики'

    def handle(self, *args, **options):
        task_name = "daily_google_reviews_update"
        
        try:
            # Перевіряємо чи вже виконувалось сьогодні
            task, created = TaskExecution.objects.get_or_create(task_name=task_name)
            current_date = now().date()
            
            if task.last_executed == current_date:
                self.stdout.write(
                    self.style.WARNING(f'Задача {task_name} вже виконувалась сьогодні ({current_date})')
                )
                return
            
            self.stdout.write(f'Починаємо щоденне оновлення Google відгуків...')
            
            # Виконуємо парсинг відгуків
            self.stdout.write('Виконуємо парсинг Google відгуків...')
            call_command('get_google_reviews')
            
            # Оновлюємо статистику
            self.stdout.write('Оновлюємо статистику відгуків...')
            call_command('update_google_review_stats')
            
            # Оновлюємо дату останнього виконання
            task.last_executed = current_date
            task.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Щоденне оновлення завершено успішно! Дата: {current_date}')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Помилка при виконанні щоденного оновлення: {e}')
            )
            logger.error(f'Помилка при виконанні щоденного оновлення: {e}')
            raise 