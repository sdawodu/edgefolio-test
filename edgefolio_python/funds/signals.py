import csv
from .models import Fund, FundImport, ImportStatus
from .serializers import FundSerializer
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=FundImport)
def extract_funds_from_csv_import(sender, instance, created, **kwargs):
    if not created:
        return

    with open(instance.file.path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        funds = []
        error_lines = []
        for line_num, row in enumerate(reader, start=1):
            serialized = FundSerializer(
                data={
                    "name": row.get("Name"),
                    "aum": row.get("AUM (USD)"),
                    "strategy": row.get("Strategy"),
                    "inception_date": row.get("Inception Date"),
                }
            )
            if serialized.is_valid():
                funds.append(
                    Fund(
                        name=serialized.data["name"],
                        aum=serialized.data["aum"],
                        strategy=serialized.data["strategy"],
                        inception_date=serialized.data["inception_date"],
                    )
                )
            else:
                error_lines.append(line_num)

        Fund.objects.bulk_create(funds)
        if error_lines:
            instance.error_summary = f"Error parsing lines: {error_lines}"
            instance.status = (
                ImportStatus.PARTIAL_SUCCESS if funds else ImportStatus.FAILED
            )
        else:
            instance.status = ImportStatus.SUCCESS

        instance.save()
