from django.db import models

class TKMK(models.Model):
    tk = models.CharField(max_length=150, unique=True)
    mk = models.CharField(max_length=255)

    class Meta:
        db_table = 'tkmk'
