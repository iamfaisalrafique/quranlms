# IslamicLMS Reference Folder Analysis Report

This document provides a deep analysis of four reference projects to inform the development of IslamicLMS v2.

---

## Folder 1: LMS Template (`D:\QuranLMS\LMS\`)

### Core Tech Stack
- **Framework:** Django (Python)
- **CSS:** Bootstrap v5.3.2, custom `style.css`
- **Icons:** FontAwesome, LineAwesome, Flaticon
- **Theme:** Edumin Saas Admin (Light/Dark mode support)

### UI/UX & Design System
- **Color Scheme:**
  - Primary: `#6a73fa` (Vibrant Indigo)
  - Secondary: `#673BB7` (Deep Purple)
  - Layout: High-contrast white backgrounds with subtle grey borders
- **Typography:**
  - Font Family: `Roboto, sans-serif` (primary), `Poppins` (headings)
  - Headings: Bold, primary color or dark grey
- **Navigation:**
  - **Top Navbar:** High (fixed), containing search, notifications, dark mode toggle, and user profile.
  - **Sidebar:** Width: `16.5rem`, MetisMenu tree structure, icons for every module.
- **Card Styles:**
  - Border Radius: `0.75rem` (12px)
  - Shadow: Soft, low-alpha box-shadow
  - Layout: Clean header/body separation

### Reusable Components
- **Dashboard Widgets:** Statistics cards (Total Students, Progress charts).
- **Forms:** Bootstrap-based validation layouts.
- **Tables:** DataTables.net integration for searching/sorting students.
- **Specific UI:** Badges for status, Alerts for notifications, Modals for Quick Add.

---

## Folder 2: Quran.com Rebuild (`D:\QuranLMS\quran.com rebuild version\`)

### Core Tech Stack
- **Framework:** Next.js (React)
- **Styling:** Styled components/Tailwind
- **Data:** API-driven (Fetching from `api.quran.com`)

### Key Features to Replicate
- **Quran Reader:** Support for Translation view vs Reading view.
- **Audio Player:** Verse-by-verse synchronization, reciter selection.
- **Search:** Deep search (text, verse number).
- **Arabic Fonts:** Extensive use of `IndoPak` and `Uthmani` fonts.

---

## Folder 3: Sunnah.com Official (`D:\QuranLMS\Sunnah dot com offical\`)

### Core Tech Stack
- **Framework:** Yii 2 (PHP)
- **Structure:** MVC (Model-View-Controller)

### Key Features to Replicate
- **Hadith Data Model:** Collections → Books → Ahadith.
- **Metadata:** Hadith grade (Sahih, Da'if), narrators, cross-references.
- **Layout:** Column-based reading view (`column1.php`).

---

## Folder 4: UKQuranAcademy PHP (`D:\QuranLMS\UKQuranAcademy_CurrentPHPProject\`)

### Core Tech Stack
- **Backend:** PHP (Native/Custom) and Node.js (SPA variant)
- **Database:** SQLite3 / MySQL (`_db.php`)
- **Real-time:** Pusher.com integration for sub-100ms chat notifications.

### Database Schema (Critical for Migration)
- **`users`:** Role-based (Admin, Teacher).
- **`students`:** `login_code` (unique ID login), `cal_email`, `status`.
- **`lessons`:** Logs `subject_type` (Quran, Hifz, etc.), `surah_page`, `ayah_range`.
- **`assignments`:** Links Teachers to Students.
- **`notifications`:** Real-time alert storage.

### Business Logic
- **Student Login:** Code-based login (no password for students).
- **Calendar Sync:** Automatic teacher assignment based on Google Calendar attendee matching.
- **Chat Filter:** Blocks emails/URLs/phone numbers in messages for security.
- **FCM:** Firebase Cloud Messaging for Push Notifications.

---

## Summary & Recommendations

### Technology Decisions
1.  **Bootstrap Version:** Use **Bootstrap 5.3+** (matching LMS template).
2.  **Arabic Fonts:** Prioritize **Scheherazade New** or **Meiryo** for clarity.
3.  **Color Palette:** Blend the LMS Indigo (`#6a73fa`) with an Islamic Green for brand consistency.
4.  **Database:** Use **PostgreSQL/MySQL** following the UKQuranAcademy schema structure.

### Priority Feature List for v2
- [ ] **LMS Core:** Student/Teacher management, Attendance, Grading.
- [ ] **Quran Integration:** Word-by-word reader with Audio playback (Ref: Quran.com).
- [ ] **Hadith Library:** Searchable Hadith database with grading (Ref: Sunnah.com).
- [ ] **Smart Logging:** Specialized inputs for Hifz/Quran progress (Ref: UKQA).
- [ ] **Real-time Alerts:** Pusher/FCM for parent-teacher communication.
