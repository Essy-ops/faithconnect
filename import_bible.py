import csv
import django
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'faithconnect.settings')
django.setup()

from church.models import BibleVerse
from datetime import date

# First load book names
book_names = {}
with open('key_english.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        book_names[row['b']] = row['n']

print(f"Loaded {len(book_names)} book names")

# Now import Bible verses
count = 0
skipped = 0

with open('t_kjv.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    verses_to_create = []

    for row in reader:
        book_num = row['b']
        chapter = row['c']
        verse_num = row['v']
        text = row['t'].strip('"')
        book_name = book_names.get(book_num, f'Book {book_num}')
        reference = f"{book_name} {chapter}:{verse_num}"

        verses_to_create.append(
            BibleVerse(
                verse=text,
                reference=reference,
                date=date.today()
            )
        )
        count += 1

        # Import in batches of 1000 for speed
        if len(verses_to_create) >= 1000:
            BibleVerse.objects.bulk_create(verses_to_create, ignore_conflicts=True)
            verses_to_create = []
            print(f"Imported {count} verses so far...")

    # Import remaining verses
    if verses_to_create:
        BibleVerse.objects.bulk_create(verses_to_create, ignore_conflicts=True)

print(f"Done! Total verses imported: {count}")