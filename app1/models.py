from django.db import models


class links_db(models.Model):

    # CHOICES = [
    #     ('com', ''),
    # ]
    link = models.URLField(max_length=20, blank=False)
    date = models.CharField(max_length=20, blank=True)
    information = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'Девайс: "{self.information}" "Ссылка: "{self.link}" Дата: "{self.date}"'


class users(models.Model):
    date = models.CharField(max_length=20, blank=True)
    information = models.CharField(max_length=20, blank=True)
    ip_1 = models.GenericIPAddressField(blank=True, null=True, unique=True)

    def __str__(self):
        return f'Девайс: "{self.information}" Дата: "{self.date}" IP: "{self.ip_1}"'


class codes(models.Model):
    user_agent = models.CharField(max_length=20, blank=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    code = models.CharField(max_length=6, blank=False)
    gmail = models.CharField(max_length=15,blank=False, null=False)
    code_sended = models.BooleanField(blank=False, null=True)

    def __str__(self):
        return f'Девайс: "{self.user_agent}" IP: "{self.ip}" Код: "{self.code}" "{self.gmail}"'
