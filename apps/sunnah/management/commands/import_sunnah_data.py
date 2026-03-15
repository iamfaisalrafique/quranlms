import os
import re
from django.core.management.base import BaseCommand
from apps.sunnah.models import HadithCollection, HadithBook, HadithChapter, Hadith

class Command(BaseCommand):
    help = 'Import Sunnah data from local SQL dump files'

    DB_PATH = r"D:\QuranLMS\Sunnah dot com offical\db"
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting local Sunnah data import..."))
        self.val_pattern = re.compile(r"'(?:\\.|[^'])*'|NULL|[\d\.-]+")

        # 1. Import Collections
        self.import_file("02-collections.sql", "Collections", self.process_collection_row)

        # 2. Import Books
        self.import_file("03-bookdata.sql", "BookData", self.process_book_row)

        # 3. Import English Hadiths from HadithTable
        self.import_file("01-hadithTable.sql", "HadithTable", self.process_hadith_row)
        
        # 4. Import Arabic Hadiths from ArabicHadithTable (to enrich/add)
        self.import_file("00-samplegitdb.sql", "ArabicHadithTable", self.process_arabic_hadith_row)

        self.stdout.write(self.style.SUCCESS("Sunnah data import complete!"))

    def parse_line_for_rows(self, line):
        rows = []
        start_indices = []
        end_indices = []
        in_string = False
        escaped = False
        for i, char in enumerate(line):
            if char == "'" and not escaped:
                in_string = not in_string
            elif char == "\\" and not escaped:
                escaped = True
                continue
            if not in_string:
                if char == '(':
                    start_indices.append(i)
                elif char == ')':
                    end_indices.append(i)
            escaped = False
        
        for start in start_indices:
            valid_end = next((e for e in end_indices if e > start), -1)
            if valid_end != -1:
                content = line[start+1:valid_end]
                matches = self.val_pattern.findall(content)
                row = []
                for m in matches:
                    if m.startswith("'") and m.endswith("'"):
                        val = m[1:-1].replace(r"\'", "'").replace(r'\"', '"').replace(r'\\', '\\').replace(r'\n', '\n')
                        row.append(val)
                    elif m == 'NULL':
                        row.append(None)
                    else:
                        row.append(m)
                if row:
                    rows.append(row)
        return rows

    def import_file(self, filename, table_name, row_callback):
        file_path = os.path.join(self.DB_PATH, filename)
        self.stdout.write(f"Processing {filename}...")
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        in_values = False
        count = 0
        search_term = table_name.lower()
        
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                lower_line = line.lower()
                if 'insert into' in lower_line and search_term in lower_line:
                    in_values = True
                    if 'values' in lower_line:
                        parts = line.split('VALUES', 1)
                        if len(parts) > 1:
                            for r in self.parse_line_for_rows(parts[1]):
                                if row_callback(r): count += 1
                    continue
                
                if in_values:
                    if line.strip().startswith('--') or not line.strip(): continue
                    current_rows = self.parse_line_for_rows(line)
                    for r in current_rows:
                        if row_callback(r): 
                            count += 1
                            if count % 1000 == 0: self.stdout.write(f"  Processed {count}...")
                    if line.strip().endswith(';'): in_values = False
        
        self.stdout.write(self.style.SUCCESS(f"  {filename}: {count} records."))

    def clean_num(self, num_str):
        if not num_str: return "0"
        s = str(num_str)
        if s.endswith('.00'): s = s[:-3]
        elif s.endswith('.0'): s = s[:-2]
        return s

    def process_collection_row(self, row):
        if len(row) < 3: return False
        HadithCollection.objects.update_or_create(slug=row[0], defaults={'name_en': row[1], 'name_ar': row[2]})
        return True

    def process_book_row(self, row):
        if len(row) < 4: return False
        try:
            col = HadithCollection.objects.get(slug=row[0])
            bnum = self.clean_num(row[1])
            HadithBook.objects.update_or_create(collection=col, book_number=bnum, defaults={'name_en': row[2], 'name_ar': row[3]})
            return True
        except: return False

    def process_hadith_row(self, row):
        if len(row) < 13: return False
        try:
            col = HadithCollection.objects.get(slug=row[0])
            bnum = self.clean_num(row[1])
            book = HadithBook.objects.get(collection=col, book_number=bnum)
            cnum = self.clean_num(row[3] or row[4] or row[2])
            chapter, _ = HadithChapter.objects.update_or_create(
                book=book, chapter_number=cnum,
                defaults={'title_en': row[12] if len(row) > 12 else "", 'title_ar': row[8] if len(row) > 8 else ""}
            )
            Hadith.objects.update_or_create(
                urn=str(row[11]),
                defaults={
                    'chapter': chapter, 'hadith_number': str(row[5]),
                    'reference_inbook': f"{bnum}:{row[5]}", 'arabic_text': row[9] if len(row) > 9 else "",
                    'text_en': row[13] if len(row) > 13 else "", 'grade': row[14] if len(row) > 14 else ""
                }
            )
            return True
        except: return False

    def process_arabic_hadith_row(self, row):
        # 0: arabicURN, 1: collection, 2: bookNumber, 6: hadithNumber, 7: hadithText, 8: babName, 12: matchingEnglishURN
        if len(row) < 13: return False
        try:
            col_slug = row[1]
            bnum = self.clean_num(row[2])
            en_urn = str(row[12]) if row[12] else f"ar-{row[0]}"
            
            col = HadithCollection.objects.get(slug=col_slug)
            book = HadithBook.objects.get(collection=col, book_number=bnum)
            cnum = self.clean_num(row[4] or row[5] or "0")
            
            chapter, _ = HadithChapter.objects.update_or_create(
                book=book, chapter_number=cnum,
                defaults={'title_ar': row[8] or ""}
            )
            
            # If hadith exists by URN, updated it, otherwise create
            Hadith.objects.update_or_create(
                urn=en_urn,
                defaults={
                    'chapter': chapter, 'hadith_number': str(row[6]),
                    'reference_inbook': f"{bnum}:{row[6]}", 'arabic_text': row[7] or ""
                }
            )
            return True
        except: return False
