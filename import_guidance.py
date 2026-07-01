import csv
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'faithconnect.settings')
django.setup()

from church.models import SpiritualGuidance

count = 0
with open('spiritual_guidance_dataset.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        SpiritualGuidance.objects.create(
            question=row['question'],
            answer=row['answer'],
            category=row['category'],
            verse_reference=row['verse_reference']
        )
        count += 1

print(f"Imported {count} spiritual guidance QA pairs!")