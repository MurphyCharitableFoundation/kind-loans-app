"""
Django settings loader for app project.
"""
import os

# Load environment-specific settings
DJANGO_ENV = os.environ.get("DJANGO_ENV", "development")

if DJANGO_ENV == "production":
    from .envs.production import *  # noqa
else:
    from .envs.development import *  # noqa
