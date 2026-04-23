# This file is superseded by the controllers/ package.
# Python loads controllers/__init__.py (the package) in preference to this
# module when both exist.  Add new route modules inside controllers/ and
# register them in controllers/__init__.py.


# ── Route modules ──────────────────────────────────────────────
from . import home   # noqa: F401  – registers the / (index) route
from . import admin  # noqa: F401  – registers /admin/pages/* routes
