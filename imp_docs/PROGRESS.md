# IslamicLMS v2.0 — Progress Tracker

**Last Updated:** Not started
**Platform Status:** 🔴 NOT STARTED

---

## How to Run

```bash
cd D:\QuranLMS\app
python manage.py runserver
# Open http://127.0.0.1:8000
```

---

## Reference Folders (Read Before Each Session)

| Folder | Read In Sessions |
|--------|-----------------|
| `D:\QuranLMS\LMS\` | 11, 12, 13, 14, 15 — Bootstrap LMS template |
| `D:\QuranLMS\quran.com rebuild version\` | 3, 13, 16 — Quran UI + data |
| `D:\QuranLMS\Sunnah dot com offical\` | 4, 14 — Sunnah UI + data |
| `D:\QuranLMS\UKQuranAcademy_CurrentPHPProject\` | 1, 2, 5, 6, 9, 10 — existing live features |
| `D:\QuranLMS\imp_docs\` | Every session — spec docs |

---

## Session Progress

| # | Focus | Model | Status | Notes |
|---|-------|-------|--------|-------|
| 1 | Django setup + settings + core models | Gemini 3 Flash | ⬜ NOT STARTED | Read: UKQuranAcademy, imp_docs |
| 2 | Auth: JWT + Google OAuth + profiles | Sonnet 4.6 Thinking | ⬜ NOT STARTED | Read: UKQuranAcademy |
| 3 | Quran models + import from api.quran.com | Gemini 3 Flash | ⬜ NOT STARTED | Read: quran.com rebuild |
| 4 | Sunnah models + import from sunnah API | Gemini 3 Flash | ⬜ NOT STARTED | Read: Sunnah dot com |
| 5 | WebSocket chat + PII filter | Sonnet 4.6 Thinking | ⬜ NOT STARTED | Read: UKQuranAcademy chat |
| 6 | Lesson log + attendance + homework | Gemini 3 Flash | ⬜ NOT STARTED | Read: UKQuranAcademy lessons |
| 7 | Quiz system + AI generation | Sonnet 4.6 Thinking | ⬜ NOT STARTED | — |
| 8 | Badges + streaks + certificate PDF | Gemini 3 Flash | ⬜ NOT STARTED | — |
| 9 | Billing: Stripe + PayPal + JazzCash | Gemini 3 Flash | ⬜ NOT STARTED | Read: UKQuranAcademy fees |
| 10 | Google Meet + FCM + Ring Alert | Sonnet 4.6 Thinking | ⬜ NOT STARTED | Read: UKQuranAcademy FCM |
| 11 | React dashboard setup + Bootstrap LMS | Gemini 3.1 Pro Low | ⬜ NOT STARTED | Read: LMS template ALL files |
| 12 | Login + student + teacher dashboard | Sonnet 4.6 Thinking | ⬜ NOT STARTED | Read: LMS index.html, students/ |
| 13 | Quran viewer + audio + word-by-word | Sonnet 4.6 Thinking | ⬜ NOT STARTED | Read: quran.com rebuild ALL |
| 14 | Sunnah browser + hadith display | Gemini 3.1 Pro Low | ⬜ NOT STARTED | Read: Sunnah dot com ALL |
| 15 | Chat UI + ring alert + notifications | Sonnet 4.6 Thinking | ⬜ NOT STARTED | Read: LMS elements/ |
| 16 | React Native: auth + dashboard + Quran | Sonnet 4.6 Thinking | ⬜ NOT STARTED | — |
| 17 | Ring alert native + FCM + chat | Sonnet 4.6 Thinking | ⬜ NOT STARTED | — |
| 18 | Docker + Coolify + production deploy | Gemini 3 Flash | ⬜ NOT STARTED | — |
| 19 | Backup + New Relic + Cloudflare | Gemini 3 Flash | ⬜ NOT STARTED | — |
| 20 | Security + performance + final | Gemini 3 Flash | ⬜ NOT STARTED | — |

---

## Session Details

### Session 1 — NOT STARTED
**Steps:** 1-5
**Model:** Gemini 3 Flash
**Read first:** `D:\QuranLMS\UKQuranAcademy_CurrentPHPProject\` + `D:\QuranLMS\imp_docs\`
**Files to create:**
- `D:\QuranLMS\app\manage.py`
- `D:\QuranLMS\app\config\settings.py`
- `D:\QuranLMS\app\config\urls.py`
- `D:\QuranLMS\app\config\asgi.py`
- `D:\QuranLMS\app\apps\accounts\models.py`
- `D:\QuranLMS\app\apps\academy\models.py`
- `D:\QuranLMS\app\requirements.txt`
- `D:\QuranLMS\app\.env.example`
- `D:\QuranLMS\app\.gitignore`
- `D:\QuranLMS\app\AGENTS.md`
- `D:\QuranLMS\app\GEMINI.md`
- `D:\QuranLMS\app\PROGRESS.md`
- `D:\QuranLMS\app\templates\index.html`

---

### Session 2 — NOT STARTED
**Steps:** 6-10
**Model:** Claude Sonnet 4.6 Thinking
**Read first:** `D:\QuranLMS\UKQuranAcademy_CurrentPHPProject\` (auth logic, student login code)
**Files to create:**
- `apps\accounts\serializers.py`
- `apps\accounts\views.py`
- `apps\accounts\urls.py`
- `apps\accounts\permissions.py`
- `apps\accounts\google_auth.py`

---

### Session 3 — NOT STARTED
**Steps:** 11-14
**Model:** Gemini 3 Flash
**Read first:** `D:\QuranLMS\quran.com rebuild version\` (data structure, API calls)
**Files to create:**
- `apps\quran\models.py`
- `apps\quran\serializers.py`
- `apps\quran\views.py`
- `apps\quran\urls.py`
- `apps\quran\management\commands\import_quran_data.py`

---

### Session 4 — NOT STARTED
**Steps:** 15-18
**Model:** Gemini 3 Flash
**Read first:** `D:\QuranLMS\Sunnah dot com offical\` (data structure, column1.php)
**Files to create:**
- `apps\sunnah\models.py`
- `apps\sunnah\serializers.py`
- `apps\sunnah\views.py`
- `apps\sunnah\urls.py`
- `apps\sunnah\management\commands\import_sunnah_data.py`

---

### Session 5 — NOT STARTED
**Steps:** 19-22
**Model:** Claude Sonnet 4.6 Thinking
**Read first:** `D:\QuranLMS\UKQuranAcademy_CurrentPHPProject\` (chat filter, Pusher logic to replace with Channels)
**Files to create:**
- `apps\chat\models.py`
- `apps\chat\consumers.py`
- `apps\chat\pii.py`
- `apps\chat\serializers.py`
- `apps\chat\views.py`
- `apps\chat\urls.py`
- `config\routing.py`

---

### Session 6 — NOT STARTED
**Steps:** 23-26
**Model:** Gemini 3 Flash
**Read first:** `D:\QuranLMS\UKQuranAcademy_CurrentPHPProject\` (lessons table, subject_type fields, ayah_range fields)
**Files to create:**
- `apps\lessons\models.py`
- `apps\attendance\models.py`
- `apps\homework\models.py`
- All serializers, views, urls for above

---

### Session 7 — NOT STARTED
**Steps:** 27-30
**Model:** Claude Sonnet 4.6 Thinking
**Files to create:**
- `apps\ai\router.py`
- `apps\quiz\models.py`
- `apps\quiz\serializers.py`
- `apps\quiz\views.py`
- `apps\quiz\urls.py`

---

### Session 8 — NOT STARTED
**Steps:** 31-34
**Model:** Gemini 3 Flash
**Files to create:**
- `apps\gamification\models.py`
- `apps\reports\certificate.py`
- `apps\reports\report_card.py`
- `templates\reports\certificate.html`
- `templates\reports\report_card.html`

---

### Session 9 — NOT STARTED
**Steps:** 35-38
**Model:** Gemini 3 Flash
**Read first:** `D:\QuranLMS\UKQuranAcademy_CurrentPHPProject\` (fees/ pages)
**Files to create:**
- `apps\billing\models.py`
- `apps\billing\stripe_views.py`
- `apps\billing\paypal_views.py`
- `apps\billing\manual_views.py`
- `apps\billing\urls.py`

---

### Session 10 — NOT STARTED
**Steps:** 39-42
**Model:** Claude Sonnet 4.6 Thinking
**Read first:** `D:\QuranLMS\UKQuranAcademy_CurrentPHPProject\` (FCM logic, calendar sync logic)
**Files to create:**
- `apps\lessons\google_workspace.py`
- `apps\notifications\fcm.py`
- `apps\notifications\ring_alert.py`
- `apps\notifications\models.py`
- `apps\notifications\urls.py`

---

### Session 11 — NOT STARTED
**Steps:** 43-47
**Model:** Gemini 3.1 Pro Low
**Read first:** `D:\QuranLMS\LMS\` — ALL template files before writing a single line
**Key LMS files to read:**
- `D:\QuranLMS\LMS\Package\templates\edumin\index.html` — main dashboard layout
- `D:\QuranLMS\LMS\doc\css\style.css` — all custom CSS variables
- `D:\QuranLMS\LMS\Package\templates\edumin\elements\` — component library
**Files to create:**
- `dashboard\package.json`
- `dashboard\vite.config.js`
- `dashboard\src\main.jsx`
- `dashboard\src\App.jsx`
- `dashboard\src\styles\theme.css`
- `dashboard\src\store\authStore.js`
- `dashboard\src\utils\api.js`

---

### Session 12 — NOT STARTED
**Steps:** 48-52
**Model:** Claude Sonnet 4.6 Thinking
**Read first:**
- `D:\QuranLMS\LMS\Package\templates\edumin\index.html`
- `D:\QuranLMS\LMS\Package\templates\edumin\students\`
- `D:\QuranLMS\LMS\Package\templates\edumin\professors\`
**Files to create:**
- `dashboard\src\pages\auth\StudentLogin.jsx`
- `dashboard\src\pages\auth\TeacherLogin.jsx`
- `dashboard\src\components\layout\Sidebar.jsx`
- `dashboard\src\components\layout\Navbar.jsx`
- `dashboard\src\pages\student\Dashboard.jsx`
- `dashboard\src\pages\teacher\Dashboard.jsx`

---

### Session 13 — NOT STARTED
**Steps:** 53-56
**Model:** Claude Sonnet 4.6 Thinking
**Read first:** `D:\QuranLMS\quran.com rebuild version\` — ALL component files
**Files to create:**
- `dashboard\src\pages\quran\SurahList.jsx`
- `dashboard\src\pages\quran\QuranViewer.jsx`
- `dashboard\src\components\quran\AudioPlayer.jsx`
- `dashboard\src\components\quran\JuzNavigator.jsx`
- `dashboard\src\components\quran\WordByWord.jsx`

---

### Session 14 — NOT STARTED
**Steps:** 57-60
**Model:** Gemini 3.1 Pro Low
**Read first:** `D:\QuranLMS\Sunnah dot com offical\` — ALL view files, especially column1.php
**Files to create:**
- `dashboard\src\pages\sunnah\Collections.jsx`
- `dashboard\src\pages\sunnah\BookList.jsx`
- `dashboard\src\pages\sunnah\HadithList.jsx`
- `dashboard\src\pages\sunnah\Search.jsx`

---

### Session 15 — NOT STARTED
**Steps:** 61-64
**Model:** Claude Sonnet 4.6 Thinking
**Read first:**
- `D:\QuranLMS\LMS\Package\templates\edumin\elements\`
- `D:\QuranLMS\UKQuranAcademy_CurrentPHPProject\` (chat UI)
**Files to create:**
- `dashboard\src\pages\chat\ChatPage.jsx`
- `dashboard\src\components\teacher\RingAlertModal.jsx`
- `dashboard\src\components\layout\NotificationBell.jsx`
- `dashboard\src\pages\quiz\QuizAttempt.jsx`

---

### Session 16 — NOT STARTED
**Steps:** 65-68
**Model:** Claude Sonnet 4.6 Thinking
**Files to create:** Full Expo project in `D:\QuranLMS\app\mobile\`

---

### Session 17 — NOT STARTED
**Steps:** 69-72
**Model:** Claude Sonnet 4.6 Thinking
**Files to create:** FCM, ring alert, chat screen in mobile/

---

### Session 18 — NOT STARTED
**Steps:** 73-76
**Model:** Gemini 3 Flash
**Files to create:** Dockerfile, docker-compose.yml, DEPLOY_CHECKLIST.md

---

### Session 19 — NOT STARTED
**Steps:** 77-80
**Model:** Gemini 3 Flash
**Files to create:** scripts/backup.sh, newrelic.ini, cloudflare docs

---

### Session 20 — NOT STARTED
**Steps:** 81-85
**Model:** Gemini 3 Flash
**Files to create:** .github/workflows/deploy.yml, README.md, final checks

---

## Files Created

*None yet — Session 1 not started*

---

## Known Issues

*None yet*

---

## Next Action

**Start Session 1:**
1. Open Antigravity
2. Select Gemini 3 Flash
3. Paste Session 1 prompt from `D:\QuranLMS\imp_docs\IslamicLMS_SessionGuide_v3.1.docx`
