#!/usr/bin/env bash
set -euo pipefail

# Run Django entirely inside your flake dev shell
nix develop -c bash -lc "
  python manage.py migrate
  python manage.py collectstatic --noinput
  gunicorn windborne_application.wsgi:application --bind 0.0.0.0:${PORT:-8000}
"
