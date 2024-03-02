from django.db import models


class Fund(models.Model):
    name = models.CharField(max_length=100)
    aum = models.DecimalField(max_digits=20, decimal_places=2)
    strategy = models.CharField(max_length=100)
    inception_date = models.DateField(blank=True)

    def __str__(self):
        return f"{self.name} : {self.strategy} : {self.inception_date}"


class ImportStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SUCCESS = "success", "Success"
    PARTIAL_SUCCESS = "partial_success", "Partial Success"
    FAILED = "failed", "Failed"

class FundImport(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField()
    status = models.CharField(
        max_length=100,
        default=ImportStatus.PENDING,
        choices=ImportStatus
    )
    error_summary = models.TextField(blank=True)

    def __str__(self):
        return f"{self.file.name} - {self.status}"