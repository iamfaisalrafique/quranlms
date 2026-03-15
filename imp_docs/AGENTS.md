# IslamicLMS v2.0 — Agent Instructions (GEMINI.md / AGENTS.md)

## ⚠️ READ THIS COMPLETELY BEFORE EVERY SINGLE TASK — NO EXCEPTIONS

---

## Project Overview

Islamic LMS SaaS platform for Quran academies.
Django 5 backend + React 18 dashboard (Bootstrap 5) + React Native mobile app.
Single PostgreSQL database. Academy scoped by foreign key. No multi-tenancy.

**Local run:** `python manage.py runserver` — that is all. Zero Docker locally.

---

## Project Location

```
D:\QuranLMS\app\
```

---

## Reference Folders — READ BEFORE RELEVANT SESSIONS

These folders are READ ONLY. Never modify them. Never delete them. Never push them to GitHub.

### 1. LMS Template — `D:\QuranLMS\LMS\`
**What it is:** Edumin SaaS Admin — Bootstrap 5.3.2 Django LMS template from Envato.
**Use for:** Every single dashboard page, every component, every layout decision.
**Critical details extracted:**
- Bootstrap version: 5.3.2
- Primary color: `#6a73fa` (override with Islamic Green `#1A6B4A`)
- Font: Roboto (body), Poppins (headings)
- Sidebar width: `16.5rem`, MetisMenu tree structure
- Card border radius: `0.75rem` (12px), soft box-shadow
- Icons: FontAwesome + LineAwesome
- Key template pages in `D:\QuranLMS\LMS\Package\templates\edumin\`:
  - `index.html` — main dashboard layout to replicate
  - `students\` — student list, student profile pages
  - `professors\` — teacher pages
  - `courses\` — course/lesson pages
  - `fees\` — billing/payment pages
  - `table\` — data table pages
  - `forms\` — form pages
  - `elements\` — UI component library
**Rule:** Before building ANY React dashboard component, open the matching HTML file in this folder and copy the exact Bootstrap classes, colors, spacing, and structure.

### 2. Quran.com Rebuild — `D:\QuranLMS\quran.com rebuild version\`
**What it is:** Next.js rebuild of quran.com frontend.
**Use for:** Quran viewer UI, audio player, word-by-word display, surah list.
**Critical details:**
- Framework: Next.js (React)
- Arabic fonts: IndoPak and Uthmani (KFGQPC)
- Features: Translation view, Reading view, verse-by-verse audio sync, reciter selection
- API source: api.quran.com
**Rule:** Before building any Quran-related React component (Sessions 13), open this folder and study the component structure, layout, and font usage.

### 3. Sunnah.com Official — `D:\QuranLMS\Sunnah dot com offical\`
**What it is:** Official Sunnah.com frontend (Yii 2 PHP MVC).
**Use for:** Hadith display layout, collection browser, grade badges, search UI.
**Critical details:**
- Column-based reading view (column1.php is the main hadith view)
- Data model: Collections → Books → Chapters → Ahadith
- Metadata: grade (Sahih/Da'if), narrator, cross-references
**Rule:** Before building any Sunnah-related React component (Session 14), open this folder and study the hadith display layout.

### 4. PHP Live Project — `D:\QuranLMS\UKQuranAcademy_CurrentPHPProject\`
**What it is:** Current live UK Quran Academy app built in PHP + Node.js.
**Use for:** Every feature that already exists and must be replicated exactly.
**Critical features confirmed from analysis:**
- Student login: code-based (no password) — maps to STU-XXXX in v2
- Lesson log: subject_type (Quran/Hifz/Tajweed/etc), surah_page, ayah_range
- Chat filter: blocks emails, URLs, phone numbers — already working
- Google Calendar sync: automatic assignment matching
- FCM push notifications: already implemented
- Pusher real-time chat: replace with Django Channels in v2
- Database tables: users, students, lessons, assignments, notifications
**Rule:** Before building any feature, check this folder first to see if it already exists in PHP and replicate the exact behavior and fields.

### 5. Important Docs — `D:\QuranLMS\imp_docs\`
**What it is:** All spec documents, session guides, analysis reports.
**Files:**
- `IslamicLMS_SessionGuide_v3.1.docx` — this session guide
- `FOLDER_ANALYSIS.md` — deep analysis of all 4 reference folders
- `AGENTS.md` — this file (copy also in project root)
- `PROGRESS.md` — session tracker (copy also in project root)
**Rule:** Read FOLDER_ANALYSIS.md before any session that touches UI or data models.

---

## Tech Stack — Final, Do Not Change

| Layer | Technology |
|-------|------------|
| Backend | Django 5.0 + Django REST Framework 3.15 |
| Realtime | Django Channels 4 (InMemoryChannelLayer locally, Redis in production) |
| Auth | JWT (djangorestframework-simplejwt) + Google OAuth |
| Database | SQLite locally → PostgreSQL 16 in production via DATABASE_URL env |
| File storage | local media/ folder → Cloudflare R2 in production via env |
| Dashboard UI | React 18 + Vite 5 + Bootstrap 5.3.2 (from LMS template) |
| Dashboard state | Zustand + TanStack Query |
| Mobile | React Native 0.74 + Expo SDK 51 |
| AI primary | Gemini Flash (via google-generativeai) |
| AI reasoning | DeepSeek R1 (via OpenAI-compatible API) |
| AI reports | Cloudflare Workers AI (free tier) |
| Task queue | Celery + Beat (production only) |
| Hosting | Contabo VPS + Coolify + Cloudflare Tunnel |
| Media CDN | Cloudflare R2 |
| Monitoring | New Relic APM (GitHub Education free) |
| Error tracking | Sentry |
| Analytics | Plausible self-hosted |

---

## Design System — From LMS Template

| Element | Value |
|---------|-------|
| Primary color | `#1A6B4A` (Islamic Green — overrides template indigo) |
| Dark green | `#14532D` |
| Gold accent | `#D4AF37` |
| Font body | Roboto, sans-serif |
| Font headings | Poppins, sans-serif |
| Font Arabic Quran | KFGQPC Uthmanic Script (NEVER change) |
| Font Arabic Hadith | Amiri, serif |
| Sidebar width | 16.5rem |
| Card border radius | 0.75rem (12px) |
| Card shadow | 0 2px 8px rgba(0,0,0,0.08) |
| Bootstrap version | 5.3.2 |
| Icon library | FontAwesome 6 + LineAwesome |

---

## Folder Structure

```
D:\QuranLMS\app\
├── manage.py                    ← entry point: python manage.py runserver
├── config/
│   ├── settings.py              ← all config via python-decouple
│   ├── urls.py                  ← all app URLs + catch-all for React
│   ├── asgi.py                  ← Django Channels WebSocket routing
│   └── wsgi.py
├── apps/
│   ├── accounts/                ← User, StudentProfile, TeacherProfile, ParentProfile
│   ├── academy/                 ← Academy, AcademySettings, tiers
│   ├── lessons/                 ← LessonLog, ClassSession, QuranBookmark, HadithBookmark
│   ├── quran/                   ← Surah, Ayat, AyatWord, Tafsir, Reciter, Juz
│   ├── sunnah/                  ← HadithCollection, Book, Chapter, Hadith
│   ├── chat/                    ← ChatRoom, ChatMessage, PII filter, WS consumer
│   ├── quiz/                    ← Quiz, Question, QuizAttempt, AttemptAnswer
│   ├── homework/                ← Homework, HomeworkAssignment
│   ├── attendance/              ← AttendanceRecord, AttendanceStreak
│   ├── gamification/            ← Badge, StudentBadge
│   ├── billing/                 ← Plan, Subscription, Payment
│   ├── notifications/           ← FCMToken, RingAlertLog
│   ├── reports/                 ← Certificate PDF, Report card PDF
│   └── ai/                      ← AIRouter class
├── dashboard/                   ← React 18 + Vite project
│   ├── src/
│   │   ├── pages/
│   │   │   ├── auth/            ← StudentLogin, TeacherLogin
│   │   │   ├── student/         ← Dashboard, Profile
│   │   │   ├── teacher/         ← Dashboard, Students, LessonLog
│   │   │   ├── quran/           ← SurahList, QuranViewer
│   │   │   ├── sunnah/          ← Collections, HadithList, Search
│   │   │   ├── chat/            ← ChatPage
│   │   │   ├── quiz/            ← QuizList, QuizAttempt
│   │   │   └── admin/           ← AcademyAdmin, SystemAdmin
│   │   ├── components/
│   │   │   ├── layout/          ← Sidebar, Navbar, NotificationBell
│   │   │   ├── quran/           ← AudioPlayer, JuzNavigator, WordByWord
│   │   │   ├── teacher/         ← RingAlertModal, LessonLogForm
│   │   │   └── common/          ← Cards, Tables, Badges, Modals
│   │   ├── store/               ← authStore.js, uiStore.js
│   │   └── utils/               ← api.js, constants.js
│   ├── package.json
│   └── vite.config.js           ← builds to ../static/dashboard/
├── mobile/                      ← React Native Expo app
├── static/                      ← compiled React build + LMS template assets
├── media/                       ← uploaded files (local dev only)
├── templates/
│   └── index.html               ← serves React dashboard
├── requirements.txt
├── .env                         ← local secrets (NEVER commit)
├── .env.example                 ← template with all variables
├── AGENTS.md                    ← this file
├── GEMINI.md                    ← same as AGENTS.md (for Antigravity)
└── PROGRESS.md                  ← always update after every task
```

---

## 20 Rules — Follow Every Single One

1. **Read AGENTS.md and PROGRESS.md before every task — no exceptions**
2. **Read the relevant reference folder before building any UI component**
3. **Update PROGRESS.md after every completed step**
4. **Never use Docker locally** — `python manage.py runserver` only
5. **Never hardcode secrets** — use python-decouple from .env file
6. **Never commit .env or .env.local** — only .env.example goes to GitHub
7. **Database**: if DATABASE_URL not set → SQLite. If set → PostgreSQL
8. **Redis/Channels**: if REDIS_URL not set → InMemoryChannelLayer. If set → Redis
9. **Celery**: only run if CELERY_ENABLED=True in env — skip completely otherwise
10. **Every new Django app** must be added to INSTALLED_APPS in settings.py
11. **Every model change** requires makemigrations before runserver
12. **Bootstrap 5.3.2 only** for dashboard — no Tailwind, no custom CSS that conflicts
13. **LMS template first** — before writing any React component, find the matching HTML in D:\QuranLMS\LMS\Package\templates\edumin\ and replicate its Bootstrap classes exactly
14. **KFGQPC Uthmanic Script** for ALL Quran Arabic text — never change this font
15. **Amiri font** for Hadith Arabic text
16. **Brand colors**: Green `#1A6B4A` | Dark `#14532D` | Gold `#D4AF37`
17. **PHP project features** must be replicated exactly — check D:\QuranLMS\UKQuranAcademy_CurrentPHPProject\ before building any feature
18. **Run python manage.py runserver** after every session to confirm no errors
19. **No print() in production code** — use Python logging module
20. **Every API endpoint** requires IsAuthenticated permission unless explicitly public

---

## Session → Reference Folder Mapping

| Session | Reference Folders to Read |
|---------|--------------------------|
| 1 | imp_docs, UKQuranAcademy_CurrentPHPProject |
| 2 | UKQuranAcademy_CurrentPHPProject (auth logic) |
| 3 | quran.com rebuild version (data structure) |
| 4 | Sunnah dot com offical (data structure) |
| 5 | UKQuranAcademy_CurrentPHPProject (chat filter logic) |
| 6 | UKQuranAcademy_CurrentPHPProject (lesson log fields) |
| 7 | UKQuranAcademy_CurrentPHPProject (quiz if exists) |
| 8 | UKQuranAcademy_CurrentPHPProject (certificates) |
| 9 | UKQuranAcademy_CurrentPHPProject (billing/fees) |
| 10 | UKQuranAcademy_CurrentPHPProject (FCM, calendar) |
| 11 | LMS (full template audit), ALL folders |
| 12 | LMS (index.html, students/, professors/) |
| 13 | quran.com rebuild version (ALL files) |
| 14 | Sunnah dot com offical (ALL files) |
| 15 | LMS (elements/, forms/), UKQuranAcademy (chat) |
| 16-17 | quran.com rebuild version, UKQuranAcademy |
| 18-20 | imp_docs |

---

## Model Selection Guide

| Task | Model |
|------|-------|
| Complex architecture, auth, WebSocket, AI router | Claude Sonnet 4.6 Thinking |
| Django models, serializers, simple CRUD views | Gemini 3 Flash |
| Complex React: dashboard, Quran viewer, chat | Claude Sonnet 4.6 Thinking |
| Bootstrap conversion from LMS template | Gemini 3.1 Pro Low |
| SVG, Lottie, design assets | Gemini 3.1 Pro High |
| React Native screens | Claude Sonnet 4.6 Thinking |
| Data import scripts, management commands | Gemini 3 Flash |
| Claude quota exhausted | Gemini 2.5 Pro (Google AI Studio free) |

---

## Local Development Commands

```bash
# Start everything
cd D:\QuranLMS\app
python manage.py runserver

# After model changes
python manage.py makemigrations
python manage.py migrate

# Import data (run once after setup)
python manage.py import_quran_data
python manage.py import_sunnah_data

# Build React dashboard (run after dashboard/ changes)
cd dashboard
npm run build
cd ..

# Create superuser
python manage.py createsuperuser
```

---

## Key URLs (local)

| URL | Purpose |
|-----|---------|
| http://127.0.0.1:8000/ | Dashboard (redirects to login) |
| http://127.0.0.1:8000/admin/ | Django admin |
| http://127.0.0.1:8000/api/ | DRF browsable API |
| http://127.0.0.1:8000/api/quran/surahs/ | Test Quran API |
| http://127.0.0.1:8000/api/sunnah/collections/ | Test Sunnah API |

---

## After Every Task — Required Checklist

- [ ] Run `python manage.py runserver` — confirm zero errors
- [ ] Update `PROGRESS.md` — mark step complete, list files changed
- [ ] If models changed — confirm migrations exist
- [ ] If dashboard changed — run `npm run build` in dashboard/
- [ ] Write: STOP — SESSION X STEP Y COMPLETE
