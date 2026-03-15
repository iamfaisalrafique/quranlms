import time
import requests
from django.core.management.base import BaseCommand
from apps.quran.models import Surah, Ayat, AyatWord, Reciter, Juz

class Command(BaseCommand):
    help = 'Import Quran data from api.quran.com'

    BASE_URL = "https://api.quran.com/api/v4"
    EN_TRANSLATION_ID = 131  # Mustafa Khattab
    UR_TRANSLATION_ID = 149  # Urdu

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting Quran data import..."))

        self.import_surahs()
        self.import_juz_data()
        self.import_reciters()
        self.import_ayat_data()

        self.stdout.write(self.style.SUCCESS("Quran data import complete!"))

    def import_surahs(self):
        self.stdout.write("Importing Surahs...")
        url = f"{self.BASE_URL}/chapters"
        response = requests.get(url).json()

        for chapter in response['chapters']:
            Surah.objects.update_or_create(
                number=chapter['id'],
                defaults={
                    'name_arabic': chapter['name_arabic'],
                    'name_english': chapter['translated_name']['name'],
                    'name_transliteration': chapter['name_simple'],
                    'revelation_type': chapter['revelation_place'].capitalize(),
                    'ayat_count': chapter['verses_count'],
                    'juz_start': chapter['pages'][0], # Placeholder, updated in next step
                    'page_start': chapter['pages'][0],
                }
            )
            self.stdout.write(f"  Imported Surah {chapter['id']}/114")
            time.sleep(0.1)

    def import_juz_data(self):
        self.stdout.write("Importing Juz data...")
        url = f"{self.BASE_URL}/juzs"
        response = requests.get(url).json()

        for juz in response['juzs']:
            mapping = juz['verse_mapping']
            first_surah = list(mapping.keys())[0]
            first_ayat = mapping[first_surah].split('-')[0]
            last_surah = list(mapping.keys())[-1]
            last_ayat = mapping[last_surah].split('-')[-1]

            Juz.objects.update_or_create(
                number=juz['juz_number'],
                defaults={
                    'name': f"Juz {juz['juz_number']}",
                    'first_surah': int(first_surah),
                    'first_ayat': int(first_ayat),
                    'last_surah': int(last_surah),
                    'last_ayat': int(last_ayat),
                }
            )
            self.stdout.write(f"  Imported Juz {juz['juz_number']}/30")

    def import_reciters(self):
        self.stdout.write("Importing Reciters...")
        url = f"{self.BASE_URL}/resources/recitations"
        response = requests.get(url).json()

        for reciter in response['recitations']:
            Reciter.objects.update_or_create(
                id=reciter['id'],
                defaults={
                    'name': reciter['reciter_name'],
                    'style': reciter['style'] or "",
                    'audio_url_pattern': f"https://audio.qurancdn.com/{reciter['id']}/"
                }
            )

    def import_ayat_data(self):
        self.stdout.write("Importing Ayat and Word data (this will take time)...")
        for surah_num in range(1, 115):
            self.stdout.write(f"Importing Surah {surah_num}/114...")
            surah = Surah.objects.get(number=surah_num)
            
            # Fetch verses with Arabic text, word-by-word, and translations
            url = f"{self.BASE_URL}/verses/by_chapter/{surah_num}"
            params = {
                'language': 'en',
                'words': 'true',
                'translations': f"{self.EN_TRANSLATION_ID},{self.UR_TRANSLATION_ID}",
                'fields': 'text_uthmani,juz_number,page_number,hizb_number,rub_number,sajdah_number',
                'word_fields': 'text_uthmani,transliteration,translation',
                'per_page': 1000  # Surah Al-Baqara is 286, so 1000 is safe
            }
            
            resp = requests.get(url, params=params).json()
            
            for v in resp['verses']:
                # Extract translations
                trans_en = next((t['text'] for t in v['translations'] if t['resource_id'] == self.EN_TRANSLATION_ID), "")
                trans_ur = next((t['text'] for t in v['translations'] if t['resource_id'] == self.UR_TRANSLATION_ID), "")
                
                ayat, created = Ayat.objects.update_or_create(
                    verse_key=v['verse_key'],
                    defaults={
                        'surah': surah,
                        'number': v['verse_number'],
                        'arabic_text': v['text_uthmani'],
                        'translation_en': trans_en,
                        'translation_ur': trans_ur,
                        'transliteration': "", # Will be filled if needed or use word-by-word
                        'juz': v['juz_number'],
                        'page': v['page_number'],
                        'sajda': v.get('sajdah_number') is not None,
                        'ruku': 0, # API doesn't provide ruku directly in this endpoint easily
                        'hizb': v['hizb_number'],
                    }
                )
                
                # Import words
                for w in v['words']:
                    if w['char_type_name'] == 'word':
                        AyatWord.objects.update_or_create(
                            ayat=ayat,
                            position=w['position'],
                            defaults={
                                'arabic': w['text_uthmani'],
                                'transliteration': w['transliteration']['text'] if w['transliteration'] else "",
                                'translation_en': w['translation']['text'] if w['translation'] else "",
                                'audio_url': f"https://audio.qurancdn.com/{w['audio_url']}" if w.get('audio_url') else ""
                            }
                        )
            
            time.sleep(0.3)
