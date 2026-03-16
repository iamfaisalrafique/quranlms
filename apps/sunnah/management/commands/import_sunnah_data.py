import os
import re
import json
import requests
import logging
import csv
import io
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
        "ahmad": "https://raw.githubusercontent.com/A7med3bdulBaset/hadith-json/v1.2.0/db/by_book/the_9_books/ahmed.json",
        "darimi": "https://raw.githubusercontent.com/A7med3bdulBaset/hadith-json/v1.2.0/db/by_book/the_9_books/darimi.json",
        "riyadussalihin": "https://raw.githubusercontent.com/AhmedBaset/hadith-json/refs/heads/main/db/by_book/other_books/riyad_assalihin.json",
        "nawawi40": "https://raw.githubusercontent.com/A7med3bdulBaset/hadith-json/v1.2.0/db/by_book/forties/nawawi40.json",
    }

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting Sunnah data import..."))

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

    def parse_sql_rows(self, values_block):
        """
        Parses a block of values from an INSERT statement using csv reader.
        This handles commas within strings correctly.
        """
        # Replace escaped single quotes with something unique
        processed = values_block.replace(r"\'", "[[ESCAPED_QUOTE]]")
        # Replace '' with something unique (SQL way of escaping ')
        processed = processed.replace("''", "[[ESCAPED_QUOTE]]")

        # We need to find each row (...), and then parse it.
        # This is tricky because strings can contain ),
        # But we've replaced escaped quotes, so we can try to find rows by logic.

        # Simpler approach: use regex to find rows, then csv to parse row content.
        # Find rows starting with ( and ending with ) followed by , or ;
        rows_raw = re.findall(r"\((.*?)\)(?:,|$)", processed, re.DOTALL)

        parsed_rows = []
        for row in rows_raw:
            # Use CSV reader to handle quoted fields and commas
            reader = csv.reader(io.StringIO(row), quotechar="'", skipinitialspace=True)
            for vals in reader:
                # Post-process to restore quotes and handle NULLs
                clean_vals = []
                for v in vals:
                    if v == 'NULL':
                        clean_vals.append(None)
                    else:
                        clean_vals.append(v.replace("[[ESCAPED_QUOTE]]", "'"))
                parsed_rows.append(clean_vals)
        return parsed_rows

    def import_collections(self):
        self.stdout.write("Fetching and parsing 02-collections.sql...")
        try:
            content = self.fetch_sql_content(self.SQL_SOURCES["collections"])
            count = 0
            match = re.search(r"INSERT INTO `Collections` .*? VALUES\s*(.*?);", content, re.DOTALL | re.IGNORECASE)
            if match:
                rows = self.parse_sql_rows(match.group(1))
                for vals in rows:
                    if len(vals) >= 21:
                        slug = vals[0]
                        HadithCollection.objects.update_or_create(
                            slug=slug,
                            defaults={
                                'collection_id': int(vals[1]) if vals[1] is not None else None,
                                'english_title': vals[3],
                                'arabic_title': vals[4] or "",
                                'num_hadith': int(vals[8]) if vals[8] is not None else 0,
                                'total_hadith': int(vals[9]) if vals[9] is not None else 0,
                                'short_intro': vals[18] or "",
                                'about': vals[19] or "",
                                'status': vals[20] or 'complete'
                            }
                        )
                        count += 1
            self.stdout.write(self.style.SUCCESS(f"✓ Collections imported: {count}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error importing collections: {e}"))
            logger.exception("Collections import failed")

    def import_books(self):
        self.stdout.write("Fetching and parsing 03-bookdata.sql...")
        try:
            content = self.fetch_sql_content(self.SQL_SOURCES["books"])
            count = 0
            match = re.search(r"INSERT INTO `BookData` .*? VALUES\s*(.*?);", content, re.DOTALL | re.IGNORECASE)
            if match:
                rows = self.parse_sql_rows(match.group(1))
                for vals in rows:
                    if len(vals) >= 27:
                        try:
                            collection = HadithCollection.objects.get(slug=vals[0])
                            HadithBook.objects.update_or_create(
                                collection=collection,
                                book_number=int(vals[18]),
                                defaults={
                                    'english_title': vals[3] or f"Book {vals[18]}",
                                    'arabic_title': vals[7] or "",
                                    'english_intro': vals[4] or "",
                                    'arabic_intro': vals[8] or "",
                                    'first_number': int(vals[22]) if vals[22] is not None else None,
                                    'last_number': int(vals[23]) if vals[23] is not None else None,
                                    'total_number': int(vals[26]) if vals[26] is not None else 0,
                                    'status': vals[27] or 'complete'
                                }
                            )
                            count += 1
                        except HadithCollection.DoesNotExist:
                            continue
                        except (ValueError, TypeError):
                            continue
            self.stdout.write(self.style.SUCCESS(f"✓ Books imported: {count}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error importing books: {e}"))
            logger.exception("Books import failed")

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

                    if (i + 1) % 1000 == 0:
                        self.stdout.write(f"  {slug}: {i+1}/{total} hadiths")

                progress[slug] = "complete"
                with open(progress_path, 'w') as f:
                    json.dump(progress, f)
                self.stdout.write(self.style.SUCCESS(f"✓ {slug} complete: {total} hadiths"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error importing {slug}: {e}"))
                logger.exception(f"Import failed for {slug}")
