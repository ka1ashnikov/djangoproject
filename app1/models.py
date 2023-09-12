from django.db import models

class links_db(models.Model):

    CHOICES = [
        ('com', ''),

    ]
    link = models.URLField(max_length=20, blank=False)
    date = models.CharField(max_length=20, blank=True)
    information = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'Девайс: "{self.information}" "Ссылка: "{self.link}" Дата: "{self.date}"'

