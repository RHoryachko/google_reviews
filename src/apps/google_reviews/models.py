from django.db import models

# Create your models here.
class GoogleReview(models.Model):
    name = models.CharField(max_length=512)
    href = models.URLField(max_length=512)
    avatar_url = models.URLField(max_length=512)
    text = models.TextField(blank=True, null=True)
    rating = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.CharField(max_length=512, null=True, blank=True)
    profile_url = models.URLField(max_length=512, null=True, blank=True)

    def __str__(self):
        return f"Review {self.name}, rating {self.text}"

    

class TaskExecution(models.Model):
    task_name = models.CharField(max_length=256)
    last_executed = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.task_name
    

class GoogleReviewStatistics(models.Model):
    date = models.DateField(auto_now_add=True)
    total_reviews = models.PositiveBigIntegerField(default=0)
    total_rating = models.PositiveBigIntegerField(default=0)
    average_rating = models.FloatField(default=0)

    def __str__(self):
        return f"Statistics for {self.date}"