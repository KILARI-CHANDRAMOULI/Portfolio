#!/usr/bin/env bash
# Publish local admin changes to the live site.
#   ./deploy.sh "added github links"
set -o errexit

MSG="${1:-Update portfolio content}"

echo "→ exporting content from the local database…"
python manage.py dumpdata core blog --indent 2 --exclude core.contactmessage > fixtures/content.json

echo "→ committing…"
rm -f .git/index.lock
git add -A
git commit -m "$MSG" || { echo "nothing changed — already up to date"; exit 0; }

echo "→ pushing (Render redeploys automatically)…"
git push

echo "✓ done. Live in ~2 minutes."
