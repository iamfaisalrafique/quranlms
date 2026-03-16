import os
import re
import json
import requests
import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.sunnah.models import HadithCollection, HadithBook, HadithChapter, Hadith

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import Sunnah data from SQL files and GitHub JSON'

    SQL_SOURCES = {
        "collections": "https://raw.githubusercontent.com/sunnah-com/website/master/db/02-collections.sql",
        "books": "https://raw.githubusercontent.com/sunnah-com/website/master/db/03-bookdata.sql",
    }

    JSON_SOURCES = {
        "bukhari": "https://raw.githubusercontent.com/A7med3bdulBaset/hadith-json/v1.2.0/db/by_book/the_9_books/bukhari.json",
        "muslim": "https://raw.githubusercontent.com/A7med3bdulBaset/hadith-json/v1.2.0/db/by_book/the_9_books/muslim.json",
        "abudawud": "https://raw.githubusercontent.com/A7med3bdulBaset/hadith-json/v1.2.0/db/by_book/the_9_books/abudawud.json",
        "tirmidhi": "https://raw.githubusercontent.com/A7med3bdulBaset/hadith-json/v1.2.0/db/by_book/the_9_books/tirmidhi.json",
        "nasai": "https://raw.githubusercontent.com/A7med3bdulBaset/hadith-json/v1.2.0/db/by_book/the_9_books/nasai.json",
        "ibnmajah": "https://raw.githubusercontent.com/A7med3bdulBaset/hadith-json/v1.2.0/db/by_book/the_9_books/ibnmajah.json",
        "malik": "https://raw.githubusercontent.com/A7med3bdulBaset/hadith-json/v1.2.0/db/by_book/the_9_books/malik.json",
        "ahmad": "https://raw.githubusercontent.com/A7med3bdulBaset/hadith-json/v1.2.0/db/by_book/the_9_books/ahmad.json",
        "darimi": "https://raw.githubusercontent.com/A7med3bdulBaset/hadith-json/v1.2.0/db/by_book/the_9_books/darimi.json",
        "riyadussalihin": "https://raw.githubusercontent.com/A7med3bdulBaset/hadith-json/v1.2.0/db/by_book/other_books/RyadSalihin.json",
        "nawawi40": "https://raw.githubusercontent.com/A7med3bdulBaset/hadith-json/v1.2.0/db/by_book/forties/nawawi40.json",
    }

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting Sunnah data import..."))
        self.val_pattern = re.compile(r"'(?:\\.|[^'])*'|NULL|[\d\.-]+")

        # 1. Parse 02-collections.sql
        self.import_collections()

        # 2. Parse 03-bookdata.sql
        self.import_books()

        # 3. Import Hadiths from JSON
        self.import_hadiths()

        self.stdout.write(self.style.SUCCESS("✓ ALL COLLECTIONS COMPLETE"))

    def fetch_sql_content(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def parse_sql_row(self, row_str):
        matches = self.val_pattern.findall(row_str)
        row = []
        for m in matches:
            if m.startswith("'") and m.endswith("'"):
                val = m[1:-1].replace(r"\'", "'").replace(r'\"', '"').replace(r'\\', '\\').replace(r'\n', '\n')
                val = val.replace("''", "'")
                row.append(val)
            elif m == 'NULL':
                row.append(None)
            else:
                row.append(m)
        return row

    def import_collections(self):
        self.stdout.write("Fetching and parsing 02-collections.sql...")
        try:
            content = self.fetch_sql_content(self.SQL_SOURCES["collections"])
            count = 0
            matches = re.findall(r"INSERT INTO .*? VALUES\s*(.*?);", content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                rows = re.findall(r"\((.*?)\),", match + ",", re.DOTALL)
                for row in rows:
                    vals = self.parse_sql_row(row)
                    # Corrected Mapping based on 02-collections.sql:
                    # (`name`, `collectionID`, `type`, `englishTitle`, `arabicTitle`, ..., `numhadith`, ..., `shortintro`, `about`, `status`, ...)
                    # Indices: 0:slug, 1:collection_id, 3:english_title, 4:arabic_title, 8:num_hadith, 18:short_intro, 20:status
                    if len(vals) >= 21:
                        slug = vals[0]
                        HadithCollection.objects.update_or_create(
                            slug=slug,
                            defaults={
                                'collection_id': int(vals[1]) if vals[1] else None,
                                'english_title': vals[3],
                                'arabic_title': vals[4] if vals[4] else "",
                                'num_hadith': int(vals[8]) if vals[8] else 0,
                                'total_hadith': int(vals[9]) if vals[9] else 0,
                                'short_intro': vals[18] if vals[18] else "",
                                'about': vals[19] if vals[19] else "",
                                'status': vals[20] if vals[20] else 'complete'
                            }
                        )
                        count += 1
            self.stdout.write(self.style.SUCCESS(f"✓ Collections imported: {count}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error importing collections: {e}"))

    def import_books(self):
        self.stdout.write("Fetching and parsing 03-bookdata.sql...")
        try:
            content = self.fetch_sql_content(self.SQL_SOURCES["books"])
            count = 0
            matches = re.findall(r"INSERT INTO .*? VALUES\s*(.*?);", content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                rows = re.findall(r"\((.*?)\),", match + ",", re.DOTALL)
                for row in rows:
                    vals = self.parse_sql_row(row)
                    if len(vals) >= 27:
                        try:
                            collection = HadithCollection.objects.get(slug=vals[0])
                            HadithBook.objects.update_or_create(
                                collection=collection,
                                book_number=int(vals[2]),
                                defaults={
                                    'english_title': vals[3] if vals[3] else f"Book {vals[2]}",
                                    'arabic_title': vals[7] if vals[7] else "",
                                    'english_intro': vals[4] if vals[4] else "",
                                    'arabic_intro': vals[8] if vals[8] else "",
                                    'first_number': int(vals[22]) if vals[22] else None,
                                    'last_number': int(vals[23]) if vals[23] else None,
                                    'total_number': int(vals[26]) if vals[26] else 0,
                                    'status': vals[27] if vals[27] else 'complete'
                                }
                            )
                            count += 1
                        except HadithCollection.DoesNotExist:
                            continue
                        except ValueError:
                            continue
            self.stdout.write(self.style.SUCCESS(f"✓ Books imported: {count}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error importing books: {e}"))

    def import_hadiths(self):
        progress_path = "import_progress.json"
        progress = {}
        if os.path.exists(progress_path):
            with open(progress_path, 'r') as f:
                progress = json.load(f)

        for slug, url in self.JSON_SOURCES.items():
            if progress.get(slug) == "complete":
                self.stdout.write(f"Skipping {slug}, already complete.")
                continue

            self.stdout.write(f"Importing {slug}...")
            try:
                collection = HadithCollection.objects.filter(slug=slug).first()
                if not collection:
                    collection = HadithCollection.objects.create(
                        slug=slug,
                        english_title=slug.replace('-', ' ').title(),
                        arabic_title=""
                    )

                response = requests.get(url)
                if response.status_code == 404:
                    self.stdout.write(self.style.WARNING(f"404 Not Found for {slug}: {url}"))
                    continue
                response.raise_for_status()

                try:
                    data = response.json()
                except json.JSONDecodeError:
                    text = response.text
                    if text.startswith('\ufeff'):
                        text = text[1:]
                    data = json.loads(text)

                hadiths_data = []
                chapters_map = {}

                if isinstance(data, dict) and "hadiths" in data:
                    hadiths_data = data["hadiths"]
                    if "chapters" in data:
                        for ch in data["chapters"]:
                            chapters_map[ch["id"]] = ch
                elif isinstance(data, list):
                    hadiths_data = data
                else:
                    self.stdout.write(self.style.ERROR(f"Unexpected JSON format for {slug}"))
                    continue

                total = len(hadiths_data)

                for i, item in enumerate(hadiths_data):
                    if not isinstance(item, dict):
                        continue

                    with transaction.atomic():
                        book_number = item.get('bookId')
                        chapter_number = str(item.get('chapterId'))

                        book, _ = HadithBook.objects.get_or_create(
                            collection=collection,
                            book_number=book_number,
                            defaults={'english_title': f"Book {book_number}", 'arabic_title': ""}
                        )

                        chapter_data = chapters_map.get(item.get('chapterId'), {})
                        chapter, _ = HadithChapter.objects.get_or_create(
                            collection=collection,
                            book=book,
                            chapter_number=chapter_number,
                            defaults={
                                'english_title': chapter_data.get('english', ""),
                                'arabic_title': chapter_data.get('arabic', "")
                            }
                        )

                        Hadith.objects.update_or_create(
                            collection=collection,
                            source_id=item['id'],
                            defaults={
                                'book': book,
                                'chapter': chapter,
                                'hadith_number': str(item.get('idInBook') or item['id']),
                                'arabic_body': item.get('arabic', ''),
                                'english_body': item.get('english', {}).get('text', ''),
                                'narrator': item.get('english', {}).get('narrator', ''),
                                'reference': f"{collection.english_title} {item.get('idInBook') or item['id']}"
                            }
                        )

                    if (i + 1) % 500 == 0:
                        self.stdout.write(f"  {slug}: {i+1}/{total} hadiths")

                progress[slug] = "complete"
                with open(progress_path, 'w') as f:
                    json.dump(progress, f)
                self.stdout.write(self.style.SUCCESS(f"✓ {slug} complete: {total} hadiths"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error importing {slug}: {e}"))
                logger.exception(f"Import failed for {slug}")
