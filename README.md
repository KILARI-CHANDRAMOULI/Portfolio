# Chandra Mouli Kilari — Developer Portfolio

A database-driven personal portfolio built with **Django 5**, **Bootstrap 5**, custom CSS and vanilla JavaScript. Every section — projects, skills, experience, education, achievements, blog posts, contact messages — is a Django model editable from the admin, so updating the site never means editing HTML.

---

## Features

- **Dark modern single-page home** — animated typing hero, scroll-reveal sections, count-up stats, scroll-spy navigation and a scroll progress bar
- **Full Django admin CMS** — inlines, custom actions, `list_editable` fields, prepopulated slugs
- **Projects** — list page with category filtering and search, plus a detail page per project
- **Blog app** — categories, tags, drafts vs published (custom `PublishedManager`), pagination, view counter, auto reading-time
- **Contact form** — server-side validation, honeypot spam trap, messages saved to the DB and readable in the admin, optional SMTP notification
- **Resume download** — served from the uploaded `Profile.resume` file with a static fallback
- **Coding profiles + GitHub stats** — LeetCode / GeeksforGeeks / HackerRank cards and live GitHub stat cards
- **Production-ready** — WhiteNoise static serving, env-based settings, security headers when `DEBUG=False`, custom 404/500 pages
- Fully responsive, keyboard accessible, and respects `prefers-reduced-motion`

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Django 5.2, Python 3.12 |
| Frontend | HTML5, CSS3, JavaScript (ES5-safe, no build step), Bootstrap 5.3 |
| Database | SQLite (dev) — swap `DATABASES` for PostgreSQL in production |
| Static files | WhiteNoise |
| Server | Gunicorn |

---

## Quick start

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env              # Windows: copy .env.example .env

# 4. Set up the database and load the CV content
python manage.py migrate
python manage.py seed_portfolio

# 5. Create your admin login
python manage.py createsuperuser

# 6. Run it
python manage.py runserver
```

- Site: <http://127.0.0.1:8000/>
- Admin: <http://127.0.0.1:8000/admin/>

---

## Project structure

```
portfolio/
├── config/                  # Project settings, root URLconf, WSGI
├── core/                    # Profile, skills, education, experience,
│   ├── models.py            #   projects, achievements, contact messages
│   ├── views.py
│   ├── admin.py
│   ├── forms.py
│   ├── context_processors.py    # Makes the active profile global
│   ├── templatetags/
│   └── management/commands/
│       └── seed_portfolio.py    # Loads all CV content
├── blog/                    # Posts, categories, published manager
├── templates/
│   ├── base.html            # Nav, footer, meta tags, asset loading
│   ├── core/                # home, project_list, project_detail
│   ├── blog/                # post_list, post_detail
│   ├── 404.html
│   └── 500.html
├── static/
│   ├── css/style.css        # Design tokens + all components
│   ├── js/main.js           # Typing, reveal, counters, scroll-spy
│   └── files/resume.pdf
└── media/                   # User uploads (profile photo, project images)
```

---

## Editing your content

Everything lives in the admin at `/admin/`:

| What you want to change | Where |
|---|---|
| Name, tagline, bio, photo, resume, social links | **Core → Profiles** |
| Skill groups and individual skills | **Core → Skill categories** (skills are inline) |
| Degrees and scores | **Core → Education** |
| Jobs and internships | **Core → Experiences** (bullets are inline) |
| Portfolio projects | **Core → Projects** |
| Awards and certifications | **Core → Achievements** |
| LeetCode / GfG / HackerRank | **Core → Coding profiles** |
| Blog articles | **Blog → Posts** |
| Messages people sent you | **Core → Contact messages** |

Two conventions worth knowing:

- A skill marked **featured** renders as an animated progress bar; the rest render as chips.
- In **Project → highlights** and **Achievement → description**, one line becomes one bullet point.

### Adding your photo and resume

Open **Core → Profiles → Chandra Mouli Kilari**, upload an image to *Photo* and a PDF to *Resume*. Both are optional — without a photo the hero shows your initials, and the Resume button falls back to `static/files/resume.pdf`.

---

## Deployment

### Render.com (easiest free option)

1. Push this repo to GitHub.
2. Create a new **Web Service** on Render pointing at the repo.
3. Build command: `./build.sh` · Start command: `gunicorn config.wsgi:application`
4. Add environment variables: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=your-app.onrender.com`, `CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com`

### PythonAnywhere

Upload the code, create a virtualenv, set the WSGI file to point at `config.wsgi`, and map `/static/` to `staticfiles/` and `/media/` to `media/`.

### Docker

```bash
docker build -t portfolio .
docker run -p 8000:8000 --env-file .env portfolio
```

### Before going live

```bash
python manage.py check --deploy
```

- Set `DEBUG=False` and a fresh `SECRET_KEY`
- Add your domain to `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`
- Run `python manage.py collectstatic`
- Switch `DATABASES` to PostgreSQL if you expect real traffic (SQLite resets on some free hosts)
- Media uploads need persistent storage (S3, Cloudinary) on ephemeral hosts

---

## Contact form email

Without SMTP credentials, messages are still **saved to the database** and visible in the admin — the email is just printed to the console. To get real email, fill the `EMAIL_*` values in `.env`. For Gmail you need an [App Password](https://myaccount.google.com/apppasswords), not your normal password.

---

## Useful commands

```bash
python manage.py seed_portfolio            # add or update seeded content
python manage.py seed_portfolio --flush    # wipe portfolio tables, then reseed
python manage.py collectstatic             # gather static files for production
python manage.py check --deploy            # production readiness audit
```

---

## License

Personal project — the code is free to reuse, but please replace the content with your own.
