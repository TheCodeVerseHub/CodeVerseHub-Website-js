"""Production settings for CodeVerseHub (Render deployment).

Usage:
  Set DJANGO_SETTINGS_MODULE=codeversehub.settings_production

Relies on environment variables (see .env.example) and falls back gracefully
for local safety. Keep secrets OUT of version control.
"""
from .settings import *  # noqa
import os
from decouple import config, Csv

# ----------------------------------------------------------------------------
# Core toggles
# ----------------------------------------------------------------------------
DEBUG = False

SECRET_KEY = config("SECRET_KEY")

_raw_allowed = config("ALLOWED_HOSTS", default="*")
if isinstance(_raw_allowed, str):
    if "," in _raw_allowed:
        ALLOWED_HOSTS = [h.strip() for h in _raw_allowed.split(",") if h.strip()]
    else:
        ALLOWED_HOSTS = [_raw_allowed.strip()]
elif isinstance(_raw_allowed, (list, tuple)):
    ALLOWED_HOSTS = list(_raw_allowed)
else:
    ALLOWED_HOSTS = ["*"]

# ----------------------------------------------------------------------------
# Security
# ----------------------------------------------------------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
_trusted = []
for _h in ALLOWED_HOSTS:
    if _h not in ("*", "localhost", "127.0.0.1"):
        # add both https and http (Render terminates SSL before app, proxy header used)
        _trusted.append(f"https://{_h}")
        _trusted.append(f"http://{_h}")
CSRF_TRUSTED_ORIGINS = _trusted

# Recommended additional hardening (can loosen if needed)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

# ----------------------------------------------------------------------------
# Static / Media
# Render ephemeral disk: collectstatic each deploy. Use WhiteNoise.
# ----------------------------------------------------------------------------
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")  # after SecurityMiddleware

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ----------------------------------------------------------------------------
# Database (Render sets DATABASE_URL). Falls back to sqlite if not provided.
# ----------------------------------------------------------------------------
import dj_database_url  # type: ignore

db_url = os.getenv("DATABASE_URL")
if db_url:
    DATABASES["default"] = dj_database_url.parse(db_url, conn_max_age=600, ssl_require=True)

# ----------------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "[%(asctime)s] %(levelname)s %(name)s:%(lineno)d :: %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}

# ----------------------------------------------------------------------------
# Email (optional placeholder; configure via env later)
# ----------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ----------------------------------------------------------------------------
# Crispy forms (unchanged) + any future production app additions
# ----------------------------------------------------------------------------
