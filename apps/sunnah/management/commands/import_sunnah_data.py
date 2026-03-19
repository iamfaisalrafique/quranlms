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
HADITH_IMPORT_BATCH_SIZE = 1000

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
        "ahmad": "https://raw.githubusercontent.com/AhmedBaset/hadith-json/v1.2.0/db/by_book/the_9_books/ahmed.json",
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
        response = requests.get(url, timeout=10)
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
        sql = self.fetch_sql_content(self.SQL_SOURCES["collections"])
        
        # Find the INSERT block
        match = re.search(r"INSERT INTO collections VALUES (.*?);", sql, re.DOTALL)
        if not match:
            self.stdout.write(self.style.ERROR("Could not find INSERT block in 02-collections.sql"))
            return

        rows = self.parse_sql_rows(match.group(1))
        
        for row in rows:
            # row format: [collection_id, name, hasbooks, haschapters, englishTitle, arabicTitle, shortIntro, about, ..., name_for_url]
            # Based on 02-collections.sql:
            # (1, 'bukhari', 'yes', 'yes', 'Sahih al-Bukhari', 'صحيح البخاري', ..., 'bukhari')
            
            # Index mapping (approximate, based on typical sunnah-com structure)
            c_id = int(row[0])
            slug = row[1]
            has_books = row[2] == 'yes'
            has_chapters = row[3] == 'yes'
            eng_title = row[4]
            ara_title = row[5]
            intro = row[6] if len(row) > 6 else ""
            about = row[7] if len(row) > 7 else ""

            obj, created = HadithCollection.objects.update_or_create(
                slug=slug,
                defaults={
                    "collection_id": c_id,
                    "english_title": eng_title,
                    "arabic_title": ara_title,
                    "short_intro": intro,
                    "about": about,
                    "has_books": has_books,
                    "has_chapters": has_chapters,
                }
            )
            if created:
                self.stdout.write(f"Created collection: {eng_title}")

    def import_books(self):
        self.stdout.write("Fetching and parsing 03-bookdata.sql...")
        sql = self.fetch_sql_content(self.SQL_SOURCES["books"])
        
        # Find the INSERT block
        match = re.search(r"INSERT INTO ookdata VALUES (.*?);", sql, re.DOTALL)
        if not match:
            self.stdout.write(self.style.ERROR("Could not find INSERT block in 03-bookdata.sql"))
            return

        rows = self.parse_sql_rows(match.group(1))
        
        for row in rows:
            # row format: [book_id, collection_id, bookNumber, englishTitle, arabicTitle, englishIntro, arabicIntro, ...]
            # (1, 1, 1, 'Revelation', 'كتاب بدء الوحى', ...)
            
            try:
                c_id = int(row[1])
                collection = HadithCollection.objects.filter(collection_id=c_id).first()
                if not collection:
                    continue

                b_num = int(row[2])
                eng_title = row[3]
                ara_title = row[4]
                eng_intro = row[5] if len(row) > 5 else ""
                ara_intro = row[6] if len(row) > 6 else ""

                HadithBook.objects.update_or_create(
                    collection=collection,
                    book_number=b_num,
                    defaults={
                        "english_title": eng_title,
                        "arabic_title": ara_title,
                        "english_intro": eng_intro,
                        "arabic_intro": ara_intro,
                    }
                )
            except (ValueError, TypeError):
                continue

    def import_hadiths(self):
        for slug, url in self.JSON_SOURCES.items():
            self.stdout.write(f"Importing hadiths for {slug}...")
            collection = HadithCollection.objects.filter(slug=slug).first()
            if not collection:
                self.stdout.write(self.style.WARNING(f"Collection {slug} not found. Skipping."))
                continue

            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                hadiths_data = data.get('hadiths', [])
                self.stdout.write(f"Found {len(hadiths_data)} hadiths for {slug}")

                batch = []
                for h in hadiths_data:
                    # JSON format: { "hadithnumber": "1", "hadithId": 1, "bookNumber": "1", "chapterId": "1", "chapterTitle": "...", "arabic": "...", "english": { "narrator": "...", "text": "..." }, "grades": [...] }
                    
                    b_num_str = h.get('bookNumber', '0')
                    try:
                        b_num = int(float(b_num_str))
                    except (ValueError, TypeError):
                        b_num = 0

                    book = HadithBook.objects.filter(collection=collection, book_number=b_num).first()
                    if not book:
                        # Create a dummy book if not found
                        book, _ = HadithBook.objects.get_or_create(
                            collection=collection,
                            book_number=b_num,
                            defaults={"english_title": f"Book {b_num}", "arabic_title": f"الكتاب {b_num}"}
                        )

                    # Handle Chapter
                    chapter = None
                    c_num = h.get('chapterId')
                    if c_num:
                        chapter, _ = HadithChapter.objects.get_or_create(
                            book=book,
                            chapter_number=str(c_num),
                            defaults={
                                "collection": collection,
                                "english_title": h.get('chapterTitle', ''),
                                "arabic_title": h.get('chapterArabic', ''), # Some JSONs might have this
                            }
                        )

                    grades_list = h.get('grades', [])
                    grade_str = ", ".join([f"{g.get('grade', '')} ({g.get('name', '')})" for g in grades_list])

                    batch.append(Hadith(
                        collection=collection,
                        book=book,
                        chapter=chapter,
                        hadith_number=str(h.get('hadithNumber', '')),
                        source_id=int(h.get('hadithId', 0)),
                        arabic_body=h.get('arabic', ''),
                        english_body=h.get('english', {}).get('text', ''),
                        narrator=h.get('english', {}).get('narrator', ''),
                        grade=grade_str,
                        reference=f"{collection.english_title} {h.get('hadithNumber', '')}"
                    ))

                    if len(batch) >= HADITH_IMPORT_BATCH_SIZE:
                        self.bulk_update_or_create_hadiths(batch)
                        batch = []

                if batch:
                    self.bulk_update_or_create_hadiths(batch)

                # Update collection counts
                collection.num_hadith = Hadith.objects.filter(collection=collection).count()
                collection.save()

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to import {slug}: {str(e)}"))

    def bulk_update_or_create_hadiths(self, hadiths):
        with transaction.atomic():
            for h in hadiths:
                Hadith.objects.update_or_create(
                    collection=h.collection,
                    source_id=h.source_id,
                    defaults={
                        "book": h.book,
                        "chapter": h.chapter,
                        "hadith_number": h.hadith_number,
                        "arabic_body": h.arabic_body,
                        "english_body": h.english_body,
                        "narrator": h.narrator,
                        "grade": h.grade,
                        "reference": h.reference,
                    }
                )
